#!/usr/bin/env bash
# unbridled — prerequisites installer.
# Does NOT log you into Beeper or touch your secrets; that's manual by design.

set -euo pipefail

log() { printf '\033[1;34m[unbridled]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[unbridled]\033[0m %s\n' "$*" >&2; }

uname_s=$(uname -s)

# 1. libolm-dev (via apt on Linux, brew on macOS)
if [ "$uname_s" = "Linux" ]; then
    if ! dpkg -l libolm-dev >/dev/null 2>&1; then
        log "installing libolm-dev (sudo required)..."
        sudo apt-get update -qq
        sudo apt-get install -y libolm-dev ffmpeg python3-venv
    else
        log "libolm-dev already installed"
    fi
elif [ "$uname_s" = "Darwin" ]; then
    if ! command -v brew >/dev/null 2>&1; then
        warn "brew not found — install Homebrew first: https://brew.sh"
        exit 1
    fi
    brew list libolm >/dev/null 2>&1 || brew install libolm ffmpeg
else
    warn "unsupported OS: $uname_s — install libolm-dev and ffmpeg manually"
fi

# 2. bbctl binary
mkdir -p ~/bin
if [ ! -x ~/bin/bbctl ]; then
    case "$uname_s" in
        Linux)  arch=$(uname -m); [ "$arch" = "x86_64" ] && arch=amd64
                url="https://github.com/beeper/bridge-manager/releases/latest/download/bbctl-linux-$arch" ;;
        Darwin) arch=$(uname -m); [ "$arch" = "x86_64" ] && arch=amd64; [ "$arch" = "arm64" ] && arch=arm64
                url="https://github.com/beeper/bridge-manager/releases/latest/download/bbctl-darwin-$arch" ;;
        *)      warn "no bbctl binary for $uname_s, skipping"; url="" ;;
    esac
    if [ -n "${url:-}" ]; then
        log "downloading bbctl from $url"
        curl -sL -o ~/bin/bbctl "$url"
        chmod +x ~/bin/bbctl
    fi
else
    log "bbctl already installed"
fi

# 3. Python venv
if [ ! -d ~/.venvs/beeper ]; then
    log "creating Python venv at ~/.venvs/beeper"
    if command -v uv >/dev/null 2>&1; then
        uv venv ~/.venvs/beeper --python 3.12
        VIRTUAL_ENV=~/.venvs/beeper uv pip install \
            'matrix-nio[e2e]' aiohttp pycryptodome cryptography pynacl \
            unpaddedbase64 canonicaljson
    else
        python3 -m venv ~/.venvs/beeper
        ~/.venvs/beeper/bin/pip install --upgrade pip
        ~/.venvs/beeper/bin/pip install \
            'matrix-nio[e2e]' aiohttp pycryptodome cryptography pynacl \
            unpaddedbase64 canonicaljson
    fi
else
    log "venv ~/.venvs/beeper already exists"
fi

# 4. Prep local state dirs
mkdir -p ~/.secrets && chmod 700 ~/.secrets
mkdir -p ~/.local/share/clawd-matrix && chmod 700 ~/.local/share/clawd-matrix

cat <<'EOF'

────────────────────────────────────────────────────────────
✓ unbridled prerequisites installed

Next steps (manual):

  1. Log in to Beeper:
       ~/bin/bbctl login
       ~/bin/bbctl whoami          # should show all bridges RUNNING

  2. Save your Beeper recovery key:
       echo 'EsXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX' \
         > ~/.secrets/beeper-recovery-key.txt
       chmod 600 ~/.secrets/beeper-recovery-key.txt

  3. Cross-sign this device:
       ~/.venvs/beeper/bin/python scripts/nio_client.py whoami
       ~/.venvs/beeper/bin/python scripts/bootstrap_crosssign.py

  4. (Recommended) Install the sync daemon:
       bash systemd/install.sh
       systemctl --user status clawd-beeper-sync

  5. Smoke test:
       ~/.venvs/beeper/bin/python scripts/nio_client.py list-chats --network messenger --limit 10

Docs:
  • README.md
  • references/setup-checklist.md
  • references/architecture.md
────────────────────────────────────────────────────────────
EOF
