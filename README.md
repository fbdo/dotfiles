# dotfiles

Managed with [chezmoi](https://chezmoi.io). Works on Linux (ChromeOS/Debian), macOS and GitHub Codespaces.

## New machine

```sh
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b ~/.local/bin init --apply fbdo
```

macOS: install [Homebrew](https://brew.sh) first; the `Brewfile` is applied automatically.

## Codespaces

Settings → Codespaces → *Automatically install dotfiles* → select this repo.
`install.sh` installs chezmoi and applies. Log: `/workspaces/.codespaces/.persistedshare/creation.log`.

## Daily use

| | |
|---|---|
| `chezmoi edit ~/.tmux.conf` | edit the source copy |
| `chezmoi diff` / `chezmoi apply` | preview / apply |
| `chezmoi add ~/.config/foo` | start tracking a file |
| `chezmoi re-add` | pull back changes made directly to (non-template) targets |
| `chezmoi update` | `git pull` + apply |
| `chezmoi cd` | shell in the source repo, to commit and push |

## Layout notes

- `~/.bashrc` / `~/.zshrc` are **not** replaced: `modify_` scripts append one line that sources `~/.config/shell/init.sh`, so distro and Codespaces defaults are kept.
- Git config lives in `~/.config/git/config`; per-machine settings go in `~/.config/git/config.local`.
- Per-machine shell additions: `~/.config/shell/local.sh`.
- Claude: `~/.claude/settings.json` is generated from a template (herdr and `lavish-axi` SessionStart hooks only when present); the herdr hook script is tracked in `~/.claude/hooks/`.
- jcode: `~/.jcode/config.toml` (template, no secrets), `preferred-tools.md` and `hooks/herdr-crew.py` are tracked; auth, sessions and caches are not. jcode env tweaks live in `~/.config/environment.d/` (ChromeOS/Linux only).
- Never tracked: SSH keys, `~/.aws`, `~/.config/gh/hosts.yml`, `~/.claude.json`, `~/.claude/.credentials.json`.
