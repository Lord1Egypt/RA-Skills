#!/bin/bash
# Start WinControl Server from WSL (runs on Windows via PowerShell 7)
# Usage: ./start.sh

cd "$(dirname "$0")"

# Create /tmp/wincontrol in WSL first
mkdir -p /tmp/wincontrol

echo "Starting WinControl Server on Windows..."
echo ""

# Check if already running
if curl -s --max-time 2 http://localhost:8767/ping > /dev/null 2>&1; then
    echo "✅ WinControl is already running!"
    echo "API: http://localhost:8767"
    echo "Frames: /tmp/wincontrol/"
    exit 0
fi

# Get WSL distro name for the path
WSL_DISTRO=$(grep -oP '(?<=^ID=).+' /etc/os-release 2>/dev/null || echo "Ubuntu")
if [ "$WSL_DISTRO" = "ubuntu" ]; then
    WSL_DISTRO="Ubuntu"
fi

# Start server using PowerShell 7 with forward-slash WSL path
PWSH='/mnt/c/Program Files/PowerShell/7/pwsh.exe'
$PWSH -Command "python //wsl.localhost/$WSL_DISTRO/home/$USER/.openclaw/workspace/skills/wincontrol/server.py" &

# Wait for startup
echo "Waiting for server to start..."
sleep 4

# Check if started
for i in 1 2 3; do
    if curl -s --max-time 2 http://localhost:8767/ping > /dev/null 2>&1; then
        echo ""
        echo "✅ WinControl started successfully!"
        echo ""
        echo "Actions API:    http://localhost:8767"
        echo "Frames:         /tmp/wincontrol/"
        echo ""
        echo "Quick test:"
        echo "  curl http://localhost:8767/ping"
        echo "  curl -X POST http://localhost:8767/capture"
        echo ""
        echo "To stop: ./stop.sh"
        exit 0
    fi
    echo "  Attempt $i/3..."
    sleep 2
done

echo ""
echo "❌ Failed to start WinControl"
exit 1
