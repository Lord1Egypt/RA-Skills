#!/usr/bin/env bash
set -euo pipefail

: "${HOME:?HOME is not set}"

ROOT="$HOME/.local/share/vennporter"
BIN="$HOME/.local/bin/vennporter"
CLI="$ROOT/dist/cli.js"

# Ensure ~/.local exists even on minimal hosts
mkdir -p "$HOME/.local" "$HOME/.local/bin" "$HOME/.local/share"

# Fail fast with clear errors
need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1" >&2; exit 1; }; }
need git
need node
need npm

if [[ ! -d "$ROOT/.git" ]]; then
  git clone --branch feat/device-code-grant --depth 1 \
    https://github.com/mansilladev/mcporter.git \
    "$ROOT"
else
  git -C "$ROOT" pull --ff-only
fi

cd "$ROOT"
if command -v pnpm >/dev/null 2>&1; then
  pnpm install
  pnpm build
else
  npm install
  npm run build
fi

cat > "$BIN" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
exec node "$HOME/.local/share/vennporter/dist/cli.js" "$@"
SH
chmod +x "$BIN"

test -f "$CLI"  # sanity check
echo "Installed: $BIN"
