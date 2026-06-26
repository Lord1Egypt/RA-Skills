#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
INSTALL_WRAPPER="$SCRIPT_DIR/install-wrapper.sh"

usage() {
  cat <<'EOF'
Usage:
  install-preset.sh --tool TOOL --host USER@HOST [--target-dir DIR]
                    [--name WRAPPER_NAME] [--remote-bin /abs/path/to/bin]
                    [--brew-prefix PREFIX] [--ssh-key KEY] [--known-hosts FILE]

Supported tools:
  imsg remindctl memo things peekaboo brew gh

Defaults:
  --target-dir defaults to OPENCLAW_BIN_DIR, then XDG_DATA_HOME/openclaw/bin,
  then HOME/.openclaw/bin.

Resolution order when --remote-bin is omitted:
  1. command -v TOOL on the remote Mac
  2. BREW_PREFIX/bin/TOOL where BREW_PREFIX comes from --brew-prefix
  3. brew --prefix on the remote Mac
  4. Common prefixes: /opt/homebrew/bin and /usr/local/bin
EOF
}

resolve_target_dir() {
  if [[ -n "${OPENCLAW_BIN_DIR:-}" ]]; then
    printf '%s\n' "$OPENCLAW_BIN_DIR"
    return
  fi
  if [[ -n "${XDG_DATA_HOME:-}" ]]; then
    printf '%s/openclaw/bin\n' "$XDG_DATA_HOME"
    return
  fi
  printf '%s/.openclaw/bin\n' "$HOME"
}

resolve_remote_bin() {
  local host="$1"
  local tool="$2"
  local brew_prefix="$3"
  local remote_script='set -e
TOOL="$1"
BREW_PREFIX="${2:-}"
if command -v "$TOOL" >/dev/null 2>&1; then
  command -v "$TOOL"
  exit 0
fi
if [[ -n "$BREW_PREFIX" && -x "$BREW_PREFIX/bin/$TOOL" ]]; then
  printf "%s/bin/%s\n" "$BREW_PREFIX" "$TOOL"
  exit 0
fi
if command -v brew >/dev/null 2>&1; then
  prefix=$(brew --prefix 2>/dev/null || true)
  if [[ -n "$prefix" && -x "$prefix/bin/$TOOL" ]]; then
    printf "%s/bin/%s\n" "$prefix" "$TOOL"
    exit 0
  fi
fi
for prefix in /opt/homebrew /usr/local; do
  if [[ -x "$prefix/bin/$TOOL" ]]; then
    printf "%s/bin/%s\n" "$prefix" "$TOOL"
    exit 0
  fi
done
exit 1'

  if ! ssh -T "$host" bash -lc "$(printf '%q' "$remote_script")" -- "$tool" "$brew_prefix"; then
    echo "Unable to resolve remote binary for preset '$tool' on $host" >&2
    echo "Pass --remote-bin explicitly if the tool is installed in a custom location." >&2
    exit 1
  fi
}

TOOL=""
HOST=""
TARGET_DIR=""
NAME=""
REMOTE_BIN=""
BREW_PREFIX=""
SSH_KEY=""
KNOWN_HOSTS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tool) TOOL="${2:-}"; shift 2 ;;
    --host) HOST="${2:-}"; shift 2 ;;
    --target-dir) TARGET_DIR="${2:-}"; shift 2 ;;
    --name) NAME="${2:-}"; shift 2 ;;
    --remote-bin) REMOTE_BIN="${2:-}"; shift 2 ;;
    --brew-prefix) BREW_PREFIX="${2:-}"; shift 2 ;;
    --ssh-key) SSH_KEY="${2:-}"; shift 2 ;;
    --known-hosts) KNOWN_HOSTS="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

[[ -n "$TOOL" && -n "$HOST" ]] || {
  usage
  exit 1
}

case "$TOOL" in
  imsg|remindctl|memo|things|peekaboo|brew|gh)
    ;;
  *)
    echo "Unsupported tool preset: $TOOL" >&2
    usage
    exit 1
    ;;
esac

TARGET_DIR="${TARGET_DIR:-$(resolve_target_dir)}"
REMOTE_BIN="${REMOTE_BIN:-$(resolve_remote_bin "$HOST" "$TOOL" "$BREW_PREFIX")}" 
wrapper_name="${NAME:-$TOOL}"

cmd=(
  "$INSTALL_WRAPPER"
  --name "$wrapper_name"
  --host "$HOST"
  --remote-bin "$REMOTE_BIN"
  --target-dir "$TARGET_DIR"
)

[[ -n "$SSH_KEY" ]] && cmd+=(--ssh-key "$SSH_KEY")
[[ -n "$KNOWN_HOSTS" ]] && cmd+=(--known-hosts "$KNOWN_HOSTS")

"${cmd[@]}"
