#!/bin/bash
# Simple Umbrel → OpenClaw proxy sync

set -e

echo "🦦 Simple Umbrel Proxy Sync"
echo "=========================="
echo

# Check Docker
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi

echo "✓ Docker is running"
echo

# Services we care about for OpenClaw
declare -A SERVICES=(
    ["perplexica"]="3444"
    ["searxng"]="8182" 
    ["synapse"]="8008"
    ["openwebui"]="10123"
)

echo "Checking OpenClaw-relevant services:"
echo "------------------------------------"

for service in "${!SERVICES[@]}"; do
    port="${SERVICES[$service]}"
    
    echo -n "🔍 $service (localhost:$port)... "
    
    # Check if proxy container exists
    if docker ps --format "{{.Names}}" | grep -q "${service}_app_proxy_1"; then
        echo -n "proxy ✓ "
        
        # Test connectivity
        if curl -s -f --max-time 3 "http://localhost:$port" > /dev/null 2>&1; then
            echo "accessible ✓"
            
            # Check OpenClaw config
            if openclaw config get "plugins.entries.${service}.config.baseUrl" 2>/dev/null | grep -q "localhost:$port"; then
                echo "  ✓ OpenClaw config is correct"
            else
                echo "  🔄 Updating OpenClaw config..."
                if openclaw config set "plugins.entries.${service}.config.baseUrl" "http://localhost:$port" > /dev/null 2>&1; then
                    echo "  ✓ Config updated"
                else
                    echo "  ⚠️  Could not update config (plugin may not be installed)"
                fi
            fi
        else
            echo "not accessible ✗"
        fi
    else
        echo "proxy not found ✗"
    fi
    
    echo
done

# Special case for matrix (uses synapse)
echo "🔍 matrix (synapse:8008)... "
if curl -s -f --max-time 3 "http://localhost:8008/_matrix/client/versions" > /dev/null 2>&1; then
    echo "  accessible ✓"
    
    # Check matrix config
    if openclaw config get "plugins.entries.matrix.config.baseUrl" 2>/dev/null | grep -q "localhost:8008"; then
        echo "  ✓ OpenClaw config is correct"
    else
        echo "  🔄 Updating matrix config..."
        if openclaw config set "plugins.entries.matrix.config.baseUrl" "http://localhost:8008" > /dev/null 2>&1; then
            echo "  ✓ Config updated"
        else
            echo "  ⚠️  Could not update matrix config"
        fi
    fi
else
    echo "  not accessible ✗"
fi

echo
echo "=== Summary ==="
echo "Services checked: ${#SERVICES[@]} + matrix"
echo
echo "Quick reference:"
echo "----------------"
echo "perplexica:  http://localhost:3444"
echo "searxng:     http://localhost:8182"
echo "synapse:     http://localhost:8008  (matrix homeserver)"
echo "openwebui:   http://localhost:10123"
echo

# Check gateway status
if systemctl is-active --quiet openclaw-gateway 2>/dev/null || pgrep -f "openclaw gateway" > /dev/null; then
    echo "⚠️  OpenClaw gateway is running"
    echo "   Restart to apply config changes: openclaw gateway restart"
else
    echo "✓ OpenClaw gateway is not running (config will apply on next start)"
fi

echo
echo "✅ Sync complete!"