#!/bin/bash
# Dual Platform Automation Setup (Mijia + HomeKit)
# Usage: bash automation_setup.sh

set -e

echo "=== Mijia + HomeKit Local Automation Setup ==="
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONF_DIR="$HOME/.config/smart-home-planner/automation/conf"
LOGS_DIR="$HOME/.config/smart-home-planner/automation/logs"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found."
    exit 1
fi

# Install dependencies
echo "[1/6] Installing dependencies..."
pip3 install mijiaAPI pyyaml requests 2>/dev/null || pip install mijiaAPI pyyaml requests

# Check Mijia auth
echo "[2/6] Checking Mijia API auth..."
AUTH_FILE="$HOME/.config/mijia-api/auth.json"
if [ -f "$AUTH_FILE" ]; then
    echo "  Mijia: auth file found"
else
    echo "  Mijia: no auth file. Login required:"
    python3 -c "from mijiaAPI import mijiaAPI; api = mijiaAPI(); api.login()"
fi

# Create config directory
echo "[3/6] Setting up config..."
mkdir -p "$CONF_DIR" "$LOGS_DIR"

for f in devices.yaml automations.yaml appdaemon.yaml; do
    if [ ! -f "$CONF_DIR/$f" ]; then
        cp "$SKILL_DIR/automation/conf/$f" "$CONF_DIR/$f"
        echo "  Created $f"
    fi
done

# Install Mijia AppDaemon plugin
echo "[4/6] Installing Mijia plugin..."
MIJIA_PLUGIN_DIR="$(python3 -c 'import appdaemon; import os; print(os.path.dirname(appdaemon.__file__))' 2>/dev/null)/plugins/mijia"
if [ -n "$MIJIA_PLUGIN_DIR" ] && [ "$MIJIA_PLUGIN_DIR" != "/plugins/mijia" ]; then
    mkdir -p "$MIJIA_PLUGIN_DIR"
    cp "$SKILL_DIR/automation/plugins/mijia/mijia_client.py" "$MIJIA_PLUGIN_DIR/"
    cp "$SKILL_DIR/automation/plugins/mijia/mijiaplugin.py" "$MIJIA_PLUGIN_DIR/"
    touch "$MIJIA_PLUGIN_DIR/__init__.py"
    echo "  Mijia plugin installed"
else
    echo "  AppDaemon not found, skipping"
fi

# Install Homebridge AppDaemon plugin
echo "[5/6] Installing Homebridge plugin..."
HOMEKIT_PLUGIN_DIR="$(python3 -c 'import appdaemon; import os; print(os.path.dirname(appdaemon.__file__))' 2>/dev/null)/plugins/homebridge"
if [ -n "$HOMEKIT_PLUGIN_DIR" ] && [ "$HOMEKIT_PLUGIN_DIR" != "/plugins/homebridge" ]; then
    mkdir -p "$HOMEKIT_PLUGIN_DIR"
    cp "$SKILL_DIR/automation/plugins/homekit/homebridgeclient.py" "$HOMEKIT_PLUGIN_DIR/"
    cp "$SKILL_DIR/automation/plugins/homekit/homebridgeplugin.py" "$HOMEKIT_PLUGIN_DIR/"
    touch "$HOMEKIT_PLUGIN_DIR/__init__.py"
    echo "  Homebridge plugin installed"
else
    echo "  AppDaemon not found, skipping"
fi

# Check Homebridge
echo "[6/6] Checking Homebridge..."
HB_URL="${HOMEBRIDGE_URL:-http://localhost:8581}"
if curl -s -o /dev/null -w "%{http_code}" "$HB_URL/api/auth/login" 2>/dev/null | grep -q "200\|401"; then
    echo "  Homebridge: reachable at $HB_URL"
else
    echo "  Homebridge: not reachable at $HB_URL"
    echo "  To install: docker run -d --name homebridge --net=host -e HOMEBRIDGE_CONFIG_UI=1 -v ~/homebridge:/homebridge homebridge/homebridge:latest"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Usage:"
echo "  Standalone (recommended):"
echo "    python3 $SKILL_DIR/automation/run_automations.py --config $CONF_DIR"
echo ""
echo "  AppDaemon:"
echo "    appdaemon -c $CONF_DIR"
echo ""
echo "  Device discovery:"
echo "    python3 $SKILL_DIR/automation/run_automations.py --discover --config $CONF_DIR"
echo "    python3 $SKILL_DIR/automation/run_automations.py --discover-homekit --config $CONF_DIR"
