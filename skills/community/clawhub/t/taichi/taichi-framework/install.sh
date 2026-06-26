#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "Installing Taichi Framework v2.1..."

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Create workspace directories
WORKSPACE_PATH=$(python3 -c "import yaml; print(yaml.safe_load(open('config.yaml'))['workspace']['path'])" 2>/dev/null || echo "./workspace")
mkdir -p "$WORKSPACE_PATH"/{logs,temp}

# Initialize state.db
touch "$WORKSPACE_PATH/state.db"

echo "Installation complete."
echo "Start with: ./start.sh"
