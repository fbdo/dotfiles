#!/bin/sh
# Bootstrap from a clone of this repo. GitHub Codespaces runs this
# automatically (non-interactively) when a codespace is created.
set -eu
src=$(cd "$(dirname "$0")" && pwd)
bin="$HOME/.local/bin"

if command -v chezmoi >/dev/null 2>&1; then
  chezmoi=$(command -v chezmoi)
else
  sh -c "$(curl -fsLS get.chezmoi.io)" -- -b "$bin"
  chezmoi="$bin/chezmoi"
fi

set -- init --apply --source="$src"
[ -t 0 ] || set -- "$@" --force --no-tty
exec "$chezmoi" "$@"
