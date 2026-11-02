#!/usr/bin/env python3
"""Open a herdr viewer pane for each jcode swarm worker, close it when the worker ends.

Wired as a global jcode hook (~/.jcode/config.toml [hooks] swarm_member_start/_end).
Workers stay headless (agent-definition tool limits keep applying); the pane only runs
`jcode --resume <worker>` as an attached client, in its own herdr tab named
"<animal> · <folder>" (for example "pig · fm-data-gc"). The tab closes when the worker ends.
Never raises, never blocks: every failure exits 0 silently. Log: ~/.jcode/state/herdr-crew.log
"""
import json, os, subprocess, sys, time

STATE = os.path.expanduser("~/.jcode/state/herdr-crew.json")
LOG = os.path.expanduser("~/.jcode/state/herdr-crew.log")
TAB_LABEL = "crew"
HERDR = os.environ.get("HERDR_BIN_PATH") or "herdr"
JCODE = os.path.expanduser("~/.local/bin/jcode")


def log(msg):
    try:
        with open(LOG, "a") as f:
            f.write("%s %s\n" % (time.strftime("%Y-%m-%dT%H:%M:%S"), msg))
    except Exception:
        pass


def herdr(*args):
    out = subprocess.run([HERDR, *args], capture_output=True, text=True, timeout=5)
    try:
        return json.loads(out.stdout or "{}").get("result") or {}
    except Exception:
        return {}


def load():
    try:
        with open(STATE) as f:
            return json.load(f)
    except Exception:
        return {}


def save(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w") as f:
        json.dump(s, f)


def live_panes():
    res = herdr("pane", "list")
    return {p.get("pane_id"): p for p in res.get("panes", [])}


def crew_tab(ws):
    for t in herdr("tab", "list", "--workspace", ws).get("tabs", []):
        if t.get("label") == TAB_LABEL:
            return t.get("tab_id")
    return None


def names(agent_id, cwd):
    """Short display name: worker animal (session_pig_... -> pig) and the folder it works in."""
    parts = agent_id.split("_")
    animal = parts[1] if len(parts) > 2 and parts[0] == "session" else agent_id[:12]
    folder = os.path.basename(os.path.normpath(cwd)) or cwd
    return animal, folder


def start(agent_id, label, cwd):
    s = load()
    panes = live_panes()
    if s.get(agent_id) in panes:
        return  # already shown (retry or resume of the same worker)
    ws = os.environ.get("HERDR_WORKSPACE_ID", "")
    animal, folder = names(agent_id, cwd)
    title = ("%s · %s" % (animal, folder))[:40]
    # One tab per worker, so the herdr sidebar shows each worker by name.
    res = herdr("tab", "create", "--workspace", ws, "--cwd", cwd, "--label", title, "--no-focus")
    pane = (res.get("root_pane") or {}).get("pane_id")
    if not pane:
        log("start %s: no pane (%s)" % (agent_id, res))
        return
    herdr("pane", "rename", pane, ("%s · %s" % (animal, label or folder))[:60])
    herdr("pane", "run", pane, "%s --resume %s" % (JCODE, agent_id))
    s[agent_id] = pane
    save(s)
    log("start %s -> %s (%s)" % (agent_id, pane, title))


def end(agent_id):
    s = load()
    pane = s.pop(agent_id, None)
    save(s)
    if pane and pane in live_panes():
        herdr("pane", "close", pane)
        log("end %s closed %s" % (agent_id, pane))


def main():
    if os.environ.get("HERDR_ENV") != "1" or os.environ.get("JCODE_HERDR_CREW") == "0":
        return
    payload = json.loads(sys.stdin.read() or "{}")
    jc = payload.get("jcode") or {}
    swarm = jc.get("swarm") if isinstance(jc.get("swarm"), dict) else {}
    event = str(jc.get("event") or os.environ.get("JCODE_HOOK_EVENT") or "")
    if not event:
        event = {"SubagentStart": "swarm_member_start", "SubagentStop": "swarm_member_end"}.get(
            str(payload.get("hook_event_name") or ""), "")
    agent_id = str(payload.get("agent_id") or "")
    if not agent_id:
        return
    if event == "swarm_member_start":
        label = str(jc.get("label") or swarm.get("label") or "")
        cwd = str(jc.get("working_dir") or swarm.get("working_dir") or payload.get("cwd") or os.getcwd())
        start(agent_id, label, cwd if os.path.isdir(cwd) else os.path.expanduser("~"))
    elif event == "swarm_member_end":
        end(agent_id)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log("error: %s" % e)
    sys.exit(0)
