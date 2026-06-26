#!/usr/bin/env bash
#
# Meshtastic Detection — One-click setup
#
# Supports: macOS, Linux (x86/arm), Raspberry Pi
#
# Usage:
#   ./setup.sh                              # auto-detect everything
#   ./setup.sh /dev/ttyUSB0                 # specify serial port
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

SERIAL_PORT="${1:-}"

# ── Color helpers ──────────────────────────────────────────────
green()  { printf '\033[32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }
red()    { printf '\033[31m%s\033[0m\n' "$*"; }
info()   { printf '  → %s\n' "$*"; }

echo ""
green "═══════════════════════════════════════════"
green "  Meshtastic Detection — Setup"
green "═══════════════════════════════════════════"
echo ""

# ── Platform detection ────────────────────────────────────────
OS_TYPE="$(uname -s)"
ARCH="$(uname -m)"
PLATFORM="unknown"

detect_platform() {
  case "$OS_TYPE" in
    Darwin)
      PLATFORM="macos"
      ;;
    Linux)
      if [[ -f /.dockerenv ]] || grep -q 'docker\|containerd' /proc/1/cgroup 2>/dev/null; then
        PLATFORM="docker"
      elif [[ -f /proc/device-tree/model ]] && grep -qi "raspberry" /proc/device-tree/model 2>/dev/null; then
        PLATFORM="rpi"
      else
        PLATFORM="linux"
      fi
      ;;
    *)
      red "Unsupported OS: $OS_TYPE"
      exit 1
      ;;
  esac
}

detect_platform
info "Platform: $PLATFORM ($OS_TYPE $ARCH)"

# ── Step 1: Find Python 3.10+ ─────────────────────────────────
PYTHON=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$candidate" &>/dev/null; then
    ver=$("$candidate" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
    major="${ver%%.*}"
    minor="${ver#*.}"
    if [[ "$major" -ge 3 && "$minor" -ge 10 ]]; then
      PYTHON="$candidate"
      break
    fi
  fi
done

if [[ -z "$PYTHON" ]]; then
  red "Error: Python 3.10+ not found."
  case "$PLATFORM" in
    macos) echo "  brew install python@3.12" ;;
    rpi)   echo "  sudo apt install python3.11 python3.11-venv" ;;
    linux) echo "  sudo apt install python3.12 python3.12-venv" ;;
  esac
  exit 1
fi

info "Using Python: $PYTHON ($($PYTHON --version 2>&1))"

# ── Step 2: Create venv ───────────────────────────────────────
if [[ ! -d venv ]]; then
  info "Creating virtual environment..."

  VENV_CREATED=false

  # 2a. Normal venv (with ensurepip)
  if "$PYTHON" -m venv venv 2>/dev/null; then
    VENV_CREATED=true
  fi

  # 2b. ensurepip 不可用时：先建无 pip 的 venv，再用 get-pip.py 装 pip（适用于 Docker 无 root）
  if [[ "$VENV_CREATED" != "true" ]]; then
    rm -rf venv
    if "$PYTHON" -m venv venv --without-pip 2>/dev/null; then
      yellow "venv created without pip; bootstrapping pip..."
      GET_PIP="$SCRIPT_DIR/.get-pip.py"
      if command -v curl &>/dev/null; then
        curl -sSL https://bootstrap.pypa.io/get-pip.py -o "$GET_PIP"
      elif command -v wget &>/dev/null; then
        wget -q -O "$GET_PIP" https://bootstrap.pypa.io/get-pip.py
      else
        "$PYTHON" -c "import urllib.request; urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', '$GET_PIP')"
      fi
      ./venv/bin/python "$GET_PIP"
      rm -f "$GET_PIP"
      VENV_CREATED=true
    fi
  fi

  # 2c. 仍失败时，在 Debian/Ubuntu 上尝试 apt 安装 python3.X-venv（需 root）
  if [[ "$VENV_CREATED" != "true" ]]; then
    rm -rf venv
    py_minor=$("$PYTHON" -c "import sys; print(sys.version_info.minor)")
    venv_pkg="python3.${py_minor}-venv"

    if command -v apt &>/dev/null; then
      yellow "ensurepip not available — trying: sudo apt install $venv_pkg ..."
      if (command -v sudo &>/dev/null && sudo apt-get update -qq && sudo apt-get install -y -qq "$venv_pkg") 2>/dev/null; then
        if "$PYTHON" -m venv venv; then
          VENV_CREATED=true
        fi
      fi
    fi

    if [[ "$VENV_CREATED" != "true" ]]; then
      red "Error: Could not create virtual environment."
      echo "  • Docker: use an image with venv (e.g. python:3.11) or run as root and install: apt install $venv_pkg"
      echo "  • Debian/Ubuntu: sudo apt install $venv_pkg"
      echo "  • Fedora: sudo dnf install python3-virtualenv"
      exit 1
    fi
  fi

  info "Virtual environment created"
else
  info "Virtual environment already exists"
fi

# ── Step 3: Install dependencies ──────────────────────────────
info "Installing Python dependencies..."
./venv/bin/pip install --upgrade pip -q 2>/dev/null || true
./venv/bin/pip install -q -r requirements.txt

# ── Step 4: Create data directory ─────────────────────────────
mkdir -p data

# ── Step 5: Detect serial port ────────────────────────────────
if [[ -z "$SERIAL_PORT" ]]; then
  case "$PLATFORM" in
    macos) SERIAL_PORT=$(ls /dev/cu.usbmodem* 2>/dev/null | head -1 || true) ;;
    *)     SERIAL_PORT=$(ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null | head -1 || true) ;;
  esac
fi

# ── Step 6: Test connection ───────────────────────────────────
if [[ -n "$SERIAL_PORT" ]]; then
  info "Detected serial port: $SERIAL_PORT"
  info "Testing Meshtastic connection..."
  if ./venv/bin/python -c "
import meshtastic, meshtastic.serial_interface
try:
    iface = meshtastic.serial_interface.SerialInterface('$SERIAL_PORT')
    node = iface.getMyNodeInfo()
    user = node.get('user', {})
    print(f'  Connected: {user.get(\"longName\", \"unknown\")} ({user.get(\"id\", \"?\")})')
    iface.close()
except Exception as e:
    print(f'  Warning: {e}')
" 2>/dev/null; then
    :
  else
    yellow "  Connection test failed — check USB cable and device"
  fi
else
  yellow "  No Meshtastic USB device detected"
  case "$PLATFORM" in
    macos) echo "  Plug in device and re-run, or: ./setup.sh /dev/cu.usbmodemXXXX" ;;
    *)     echo "  Plug in device and re-run, or: ./setup.sh /dev/ttyUSB0" ;;
  esac
fi

# ── Step 7: Generate service file ─────────────────────────────
generate_service() {
  local install_dir="$SCRIPT_DIR"
  local run_user
  run_user="$(whoami)"
  local port="${SERIAL_PORT:-__SERIAL_PORT__}"

  case "$PLATFORM" in
    macos)
      local plist_template="$SCRIPT_DIR/references/com.openclaw.meshtastic-detection.plist"
      local plist_out="$SCRIPT_DIR/com.openclaw.meshtastic-detection.plist"

      if [[ ! -f "$plist_template" ]]; then
        yellow "  Skipping service generation: plist template not found"
        return
      fi

      sed \
        -e "s|__INSTALL_DIR__|${install_dir}|g" \
        -e "s|__SERIAL_PORT__|${port}|g" \
        -e "s|__USER__|${run_user}|g" \
        "$plist_template" > "$plist_out"

      info "Generated: com.openclaw.meshtastic-detection.plist"
      echo ""
      echo "  Install as macOS service (launchd):"
      echo "    cp com.openclaw.meshtastic-detection.plist ~/Library/LaunchAgents/"
      echo "    launchctl load ~/Library/LaunchAgents/com.openclaw.meshtastic-detection.plist"
      echo ""
      echo "  Uninstall:"
      echo "    launchctl unload ~/Library/LaunchAgents/com.openclaw.meshtastic-detection.plist"
      ;;

    docker)
      local ep_template="$SCRIPT_DIR/references/entrypoint.sh"
      local ep_out="$SCRIPT_DIR/entrypoint.sh"

      if [[ ! -f "$ep_template" ]]; then
        yellow "  Skipping entrypoint generation: template not found"
        return
      fi

      sed \
        -e "s|__INSTALL_DIR__|${install_dir}|g" \
        -e "s|__SERIAL_PORT__|${port}|g" \
        "$ep_template" > "$ep_out"
      chmod +x "$ep_out"

      info "Generated: entrypoint.sh (Docker background runner)"
      echo ""
      echo "  Inside container — run in background:"
      echo "    nohup ./entrypoint.sh > data/entrypoint.log 2>&1 &"
      echo ""
      echo "  Or use as container CMD (docker-compose.yml):"
      echo "    command: ./entrypoint.sh"
      echo ""
      echo "  Check logs:"
      echo "    tail -f data/entrypoint.log"
      ;;

    linux|rpi)
      local svc_template="$SCRIPT_DIR/references/meshtastic-detection.service"
      local svc_out="$SCRIPT_DIR/meshtastic-detection.generated.service"

      if [[ ! -f "$svc_template" ]]; then
        yellow "  Skipping service generation: systemd template not found"
        return
      fi

      sed \
        -e "s|__INSTALL_DIR__|${install_dir}|g" \
        -e "s|__SERIAL_PORT__|${port}|g" \
        -e "s|__USER__|${run_user}|g" \
        "$svc_template" > "$svc_out"

      info "Generated: meshtastic-detection.generated.service"
      echo ""
      echo "  Install as systemd service:"
      echo "    sudo cp meshtastic-detection.generated.service /etc/systemd/system/meshtastic-detection.service"
      echo "    sudo systemctl daemon-reload"
      echo "    sudo systemctl enable --now meshtastic-detection"
      echo ""
      echo "  Check status:"
      echo "    sudo systemctl status meshtastic-detection"
      echo "    sudo journalctl -u meshtastic-detection -f"
      ;;
  esac
}

generate_service

# ── Step 8: Serial port permissions (bare-metal Linux only) ───
if [[ "$PLATFORM" == "linux" || "$PLATFORM" == "rpi" ]]; then
  if ! groups 2>/dev/null | grep -q dialout; then
    echo ""
    yellow "  Note: your user may need serial port access."
    echo "    sudo usermod -a -G dialout $(whoami)"
    echo "    (log out and back in after running this)"
  fi
fi

# ── Done ──────────────────────────────────────────────────────
echo ""
green "═══════════════════════════════════════════"
green "  Setup complete!  ($PLATFORM)"
green "═══════════════════════════════════════════"
echo ""
if [[ "$PLATFORM" == "docker" ]]; then
  echo "  Run in background (inside container):"
  echo "    nohup ./entrypoint.sh > data/entrypoint.log 2>&1 &"
  echo ""
  echo "  Or set as container CMD in docker-compose.yml:"
  echo "    command: ./entrypoint.sh"
else
  echo "  Start the receiver:"
  if [[ -n "$SERIAL_PORT" ]]; then
    echo "    ./venv/bin/python scripts/usb_receiver.py --port $SERIAL_PORT"
  else
    case "$PLATFORM" in
      macos) echo "    ./venv/bin/python scripts/usb_receiver.py --port /dev/cu.usbmodemXXXX" ;;
      *)     echo "    ./venv/bin/python scripts/usb_receiver.py --port /dev/ttyUSB0" ;;
    esac
  fi
fi
echo ""
echo "  Check alerts:"
echo "    ./venv/bin/python scripts/event_monitor.py"
echo ""
echo "  Query data:"
echo "    ./venv/bin/python scripts/sensor_cli.py latest"
echo ""
