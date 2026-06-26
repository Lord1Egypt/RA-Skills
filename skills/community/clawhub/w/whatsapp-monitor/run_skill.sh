#!/usr/bin/env bash
# WhatsApp Monitor Skill - OpenClaw integration (Linux/macOS)
set -euo pipefail

echo "========================================"
echo "WhatsApp Monitor Skill - OpenClaw Integration"
echo "========================================"
echo

if [[ -z "${OPENCLAW_HOME:-}" ]]; then
  echo "[INFO] OPENCLAW_HOME environment variable not set"
  echo "[INFO] Using current directory: ${PWD}"
  SKILL_DIR="${PWD}"
else
  echo "[INFO] OPENCLAW_HOME: ${OPENCLAW_HOME}"
  SKILL_DIR="${OPENCLAW_HOME}/skills/whatsapp-monitor"
fi

echo "[INFO] Skill directory: ${SKILL_DIR}"
echo

if command -v python3 &>/dev/null; then
  PYTHON=python3
elif command -v python &>/dev/null; then
  PYTHON=python
else
  echo "[ERROR] Python not found. Please install Python 3.8+"
  exit 1
fi

cd "${SKILL_DIR}"

if ! "${PYTHON}" -c "import aiohttp, pydantic, yaml, requests" &>/dev/null; then
  echo "[WARNING] Some dependencies missing. Installing..."
  if ! "${PYTHON}" -m pip install -r requirements.txt --quiet; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
  fi
  echo "[OK] Dependencies installed"
fi

ACTION="${1:-help}"
EXIT_CODE=0

case "${ACTION}" in
  help)
    echo "Usage: $0 [command]"
    echo
    echo "Commands:"
    echo "  start     - Start monitoring"
    echo "  status    - Show status"
    echo "  test      - Test configuration"
    echo "  export    - Force export to Feishu"
    echo "  config    - Show configuration"
    echo "  setup     - Run setup wizard"
    echo "  help      - Show this help"
    ;;
  start)
    echo "[INFO] Starting WhatsApp Monitor..."
    "${PYTHON}" scripts/monitor.py --start
    ;;
  status)
    echo "[INFO] Checking WhatsApp Monitor status..."
    "${PYTHON}" scripts/monitor.py --status
    ;;
  test)
    echo "[INFO] Testing WhatsApp Monitor configuration..."
    "${PYTHON}" scripts/monitor.py --test-config
    ;;
  export)
    echo "[INFO] Force exporting messages to Feishu..."
    "${PYTHON}" scripts/monitor.py --export
    ;;
  config)
    echo "[INFO] Showing configuration..."
    echo
    echo "=== WhatsApp Targets ==="
    if [[ -f config/whatsapp-targets.json ]]; then
      cat config/whatsapp-targets.json
    else
      echo "Config file not found"
    fi
    echo
    echo "=== Feishu Settings ==="
    if [[ -f config/feishu-settings.json ]]; then
      cat config/feishu-settings.json
    else
      echo "Config file not found"
    fi
    ;;
  setup)
    echo "[INFO] Running setup wizard..."
    "${PYTHON}" scripts/setup.py
    ;;
  *)
    echo "[ERROR] Unknown command: ${ACTION}"
    echo "Use '$0 help' for usage information"
    EXIT_CODE=1
    ;;
esac

echo
echo "========================================"
echo "Skill execution completed"
echo "========================================"

if [[ -t 0 ]] && [[ -t 1 ]]; then
  read -r -p "Press Enter to continue..."
fi

exit "${EXIT_CODE}"
