#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$HOME/.local/share/vibe-prompt-compiler-portable}"

mkdir -p "$TARGET_DIR"
cp -R "$SCRIPT_DIR/"* "$TARGET_DIR/"
chmod +x "$TARGET_DIR/scripts/compile_prompt.py" "$TARGET_DIR/scripts/create_handoff.py" || true

cat <<EOF
Installed vibe-prompt-compiler-portable to:
  $TARGET_DIR

Quick test:
  python3 "$TARGET_DIR/scripts/compile_prompt.py" --request "Build an admin dashboard MVP" --stack "Next.js, Supabase, Tailwind"

Handoff test:
  python3 "$TARGET_DIR/scripts/create_handoff.py" --request "Fix login API 500" --mode bugfix --output handoff
EOF
