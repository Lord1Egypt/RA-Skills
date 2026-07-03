#!/bin/bash
# ==============================================================================
# Server-Mate Node One-Key Bootstrap Script
# ==============================================================================
set -e

echo "=== Server-Mate Bootstrap Start ==="

# Check root privilege
if [ "$EUID" -ne 0 ]; then
  echo "Error: Please run as root (sudo)."
  exit 1
fi

# Detect package manager
if [ -x "$(command -v apt-get)" ]; then
  PKG_MANAGER="apt"
elif [ -x "$(command -v yum)" ]; then
  PKG_MANAGER="yum"
else
  echo "Error: Supported package manager (apt or yum) not found."
  exit 1
fi

echo "Detected package manager: $PKG_MANAGER"

# Install Python3, Git and pip
echo "Installing prerequisites..."
if [ "$PKG_MANAGER" = "apt" ]; then
  apt-get update -y
  apt-get install -y python3 python3-pip git python3-venv fonts-noto-cjk
elif [ "$PKG_MANAGER" = "yum" ]; then
  yum install -y python3 python3-pip git google-noto-sans-cjk-ttc-fonts
fi

# Create target directory
TARGET_DIR="/opt/server-mate"
echo "Cloning Server-Mate repository to $TARGET_DIR..."
if [ -d "$TARGET_DIR" ]; then
  echo "Target directory $TARGET_DIR already exists. Updating..."
  cd "$TARGET_DIR"
  git pull
else
  git clone https://github.com/tankeito/server-mate.git "$TARGET_DIR"
  cd "$TARGET_DIR"
fi

# Setup Virtual Environment (Optional but recommended for modern Python PEP 668)
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing Python library dependencies..."
pip install --upgrade pip
pip install psutil pyyaml requests matplotlib geoip2 maxminddb aiohttp

# Prepare Config
if [ ! -f "config.yaml" ]; then
  echo "Creating config.yaml from example..."
  cp config.example.yaml config.yaml
  # Replace default host_id with system hostname
  HOSTNAME=$(hostname)
  sed -i "s/host_id: web-01/host_id: $HOSTNAME/g" config.yaml
  echo "Config file initialized. Please configure Nginx/Apache logs and webhook endpoints in $TARGET_DIR/config.yaml later."
else
  echo "config.yaml already exists. Skipping config initialization."
fi

# Generate and register Systemd service
echo "Registering systemd service..."
# Execute via the venv Python to embed the correct path
python3 scripts/server_agent.py --config ./config.yaml --generate-service > /etc/systemd/system/server-mate.service

# Reload and start service
echo "Starting Server-Mate daemon..."
systemctl daemon-reload
systemctl enable server-mate.service
systemctl restart server-mate.service

echo "=============================================================================="
echo "✓ Server-Mate successfully installed and started!"
echo "✓ Status Check: systemctl status server-mate.service"
echo "✓ Config Path: $TARGET_DIR/config.yaml"
echo "✓ Visual Dashboard is enabled on http://0.0.0.0:8000 by default (if set in config)."
echo "=============================================================================="
