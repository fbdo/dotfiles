# Shared setup for bash and zsh, sourced from ~/.bashrc and ~/.zshrc.
# Keep it POSIX sh. Per-machine additions go in ~/.config/shell/local.sh (not tracked).

case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *) export PATH="$HOME/.local/bin:$PATH" ;;
esac

# Homebrew (macOS)
if [ -x /opt/homebrew/bin/brew ]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ] && [ "$(uname)" = Darwin ]; then
  eval "$(/usr/local/bin/brew shellenv)"
fi

# Prefer helix; in Codespaces keep the VS Code editor it configures
if [ -z "${CODESPACES:-}" ] && command -v hx >/dev/null 2>&1; then
  export EDITOR=hx VISUAL=hx
fi

# nvm: skip if the image already loaded it (Codespaces does)
if ! command -v nvm >/dev/null 2>&1; then
  if [ -z "${NVM_DIR:-}" ]; then
    if [ -d "${XDG_CONFIG_HOME:-$HOME/.config}/nvm" ]; then
      export NVM_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/nvm"
    else
      export NVM_DIR="$HOME/.nvm"
    fi
  fi
  [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
  [ -n "${BASH_VERSION:-}" ] && [ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"
fi

[ -r "${XDG_CONFIG_HOME:-$HOME/.config}/shell/local.sh" ] && . "${XDG_CONFIG_HOME:-$HOME/.config}/shell/local.sh"
true
