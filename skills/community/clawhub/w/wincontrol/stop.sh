#!/bin/bash
# Stop WinControl Server

echo "Stopping WinControl..."

# Kill Python process on Windows using PowerShell 7
PWSH='/mnt/c/Program Files/PowerShell/7/pwsh.exe'
$PWSH -Command "Get-Process python -ErrorAction SilentlyContinue | Where-Object {\$_.CommandLine -like '*wincontrol*'} | Stop-Process -Force" 2>/dev/null

# Clean up frames
rm -rf /tmp/wincontrol/*.jpg 2>/dev/null

# Verify stopped
if curl -s --max-time 1 http://localhost:8767/ping > /dev/null 2>&1; then
    echo "⚠️  Server may still be running"
else
    echo "✅ WinControl stopped"
fi
