#!/usr/bin/env bash
# Install WhatsApp Monitor Skill dependencies (Linux/macOS)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

echo "Installing WhatsApp Monitor Skill dependencies..."
echo

if command -v python3 &>/dev/null; then
  PYTHON=python3
elif command -v python &>/dev/null; then
  PYTHON=python
else
  echo "Error: Python not found. Please install Python 3.8+."
  exit 1
fi

"${PYTHON}" --version

for pkg in pyyaml aiohttp pydantic requests python-dateutil; do
  echo "Installing ${pkg}..."
  "${PYTHON}" -m pip install "${pkg}" --quiet
done

echo
echo "All dependencies installed successfully!"
echo

echo "Running skill test..."
"${PYTHON}" test_skill.py

echo
if [[ -t 0 ]] && [[ -t 1 ]]; then
  read -r -p "Press Enter to continue..."
fi
