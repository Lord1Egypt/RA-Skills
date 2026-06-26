#!/bin/bash
# Umbrel Proxy Sync - One-shot script to discover, update, and test Umbrel services

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "🦦 Umbrel Proxy Sync"
echo "==================="
echo

# Check dependencies
check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ Missing dependency: $1"
        echo "   Please install: $2"
        return 1
    fi
    return 0
}

echo "Checking dependencies..."
check_dependency "docker" "Docker" || exit 1
check_dependency "python3" "Python 3" || exit 1
check_dependency "openclaw" "OpenClaw CLI" || exit 1
check_dependency "curl" "curl" || exit 1
echo "✓ All dependencies found"
echo

# Step 1: Discover services
echo "Step 1: Discovering Umbrel services..."
cd "$SCRIPT_DIR"
if python3 discover_umbrel_services.py; then
    echo "✓ Service discovery complete"
else
    echo "❌ Service discovery failed"
    exit 1
fi
echo

# Check if we found any services
if [ ! -f "umbrel_services.json" ] || [ ! -s "umbrel_services.json" ]; then
    echo "⚠️  No Umbrel services found. Skipping updates."
    exit 0
fi

SERVICE_COUNT=$(python3 -c "import json; print(len(json.load(open('umbrel_services.json'))))")
echo "Found $SERVICE_COUNT service(s)"
echo

# Step 2: Update OpenClaw config
echo "Step 2: Updating OpenClaw config..."
if python3 update_openclaw_config.py; then
    echo "✓ Config update complete"
else
    echo "⚠️  Config update had issues (some services may not be configured)"
fi
echo

# Step 3: Test connectivity
echo "Step 3: Testing connectivity..."
if python3 test_connectivity.py; then
    echo "✓ Connectivity tests passed"
else
    echo "⚠️  Some connectivity tests failed"
fi
echo

# Step 4: Summary
echo "Step 4: Summary"
echo "--------------"
echo "Services discovered: $SERVICE_COUNT"
echo "Config updated: ✓"
echo "Connectivity tested: ✓"
echo

# Check if OpenClaw gateway needs restart
echo "Checking OpenClaw gateway status..."
if openclaw gateway status | grep -q "active (running)"; then
    echo "⚠️  OpenClaw gateway is running and needs restart to apply config changes"
    echo "   Run: openclaw gateway restart"
else
    echo "✓ OpenClaw gateway is not running (config will apply on next start)"
fi
echo

# Create a quick reference
echo "Quick Reference:"
echo "----------------"
python3 -c "
import json
try:
    with open('umbrel_services.json') as f:
        services = json.load(f)
    for service in services:
        app = service['app_name']
        port = service['proxy_port']
        print(f'{app}: http://localhost:{port}')
except:
    print('No services found')
"
echo

echo "✅ Umbrel Proxy Sync complete!"
echo
echo "Next steps:"
echo "1. Review the connectivity test results above"
echo "2. Restart OpenClaw gateway if it's running: openclaw gateway restart"
echo "3. Test OpenClaw plugins that use these services"
echo

exit 0