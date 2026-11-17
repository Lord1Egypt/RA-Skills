#!/usr/bin/env bash
#
# Install the session-scoped Xinling runtime.
#
# This installer copies runtime files only. It does not change agent identity
# files, shell profiles, permissions, or external credentials.

set -euo pipefail

XINLING_DIR="${XINLING_HOME:-$HOME/.xinling-bushou-v2}"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Installing xinling-bushou-v2 into: $XINLING_DIR"
mkdir -p "$XINLING_DIR"

for directory in core adapters schemas personas; do
    mkdir -p "$XINLING_DIR/$directory"
    cp -R "$PROJECT_DIR/$directory/." "$XINLING_DIR/$directory/"
done

mkdir -p "$XINLING_DIR/bin"
cp "$PROJECT_DIR/scripts/xinling" "$XINLING_DIR/bin/xinling"
chmod 0755 "$XINLING_DIR/bin/xinling"

python3 - "$XINLING_DIR" <<'PY'
import sys
from pathlib import Path

install_dir = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(install_dir))

from core.persona_engine import PersonaEngine

engine = PersonaEngine(base_dir=install_dir)
personas = engine.list_personas()
print(f"Installed {len(personas)} personas.")
print("Activation is explicit and session-scoped.")
print(f"CLI: {install_dir / 'bin' / 'xinling'} list")
PY
