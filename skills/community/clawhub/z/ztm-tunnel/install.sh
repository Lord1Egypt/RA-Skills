#!/bin/bash
# ZTM Tunnel Skill Installation Script
# This script installs ZTM and configures it for use with the ztm-tunnel skill

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔌 ZTM Tunnel Skill Installer${NC}"
echo "=================================="

# Check if running on macOS or Linux
OS=$(uname -s)
if [[ "$OS" != "Darwin" && "$OS" != "Linux" ]]; then
    echo -e "${RED}❌ Unsupported OS: $OS${NC}"
    exit 1
fi

# Detect architecture
ARCH=$(uname -m)
case "$ARCH" in
    x86_64)
        ZTM_ARCH="generic_linux-x86_64"
        ;;
    arm64|aarch64)
        ZTM_ARCH="generic_linux-arm64"
        ;;
    *)
        echo -e "${RED}❌ Unsupported architecture: $ARCH${NC}"
        exit 1
        ;;
esac

echo -e "${YELLOW}📦 Step 1: Checking ZTM installation...${NC}"

# Check if ztm is already installed
if command -v ztm &> /dev/null; then
    ZTM_VERSION=$(ztm version 2>/dev/null | head -1 || echo "unknown")
    echo -e "${GREEN}✅ ZTM already installed: $ZTM_VERSION${NC}"
else
    echo -e "${YELLOW}📥 Installing ZTM...${NC}"
    
    # Create temp directory
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    # Get latest version from GitHub
    LATEST_VERSION=$(curl -s https://api.github.com/repos/flomesh-io/ztm/releases/latest | grep -o '"tag_name":.*' | cut -d'"' -f4)
    
    if [[ -z "$LATEST_VERSION" ]]; then
        echo -e "${RED}❌ Could not get latest ZTM version${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}   Latest version: $LATEST_VERSION${NC}"
    
    # Download
    FILENAME="ztm-aio-${LATEST_VERSION}-${ZTM_ARCH}.tar.gz"
    DOWNLOAD_URL="https://github.com/flomesh-io/ztm/releases/download/${LATEST_VERSION}/${FILENAME}"
    
    echo -e "${BLUE}   Downloading $DOWNLOAD_URL...${NC}"
    
    if curl -L -o "$FILENAME" "$DOWNLOAD_URL" 2>/dev/null; then
        # Extract
        tar -xzf "$FILENAME"
        
        # Install to /usr/local/bin (requires sudo)
        if [[ -w /usr/local/bin ]]; then
            mv bin/ztm /usr/local/bin/ztm
            chmod +x /usr/local/bin/ztm
        else
            echo -e "${YELLOW}   Note: Need sudo to install to /usr/local/bin${NC}"
            sudo mv bin/ztm /usr/local/bin/ztm
            sudo chmod +x /usr/local/bin/ztm
        fi
        
        echo -e "${GREEN}✅ ZTM installed successfully!${NC}"
    else
        echo -e "${RED}❌ Failed to download ZTM${NC}"
        exit 1
    fi
    
    # Cleanup
    cd /
    rm -rf "$TEMP_DIR"
fi

# Verify installation
echo -e "${YELLOW}🔍 Step 2: Verifying ZTM...${NC}"
ztm version

echo -e "${YELLOW}🚀 Step 3: Starting ZTM Agent...${NC}"

# Check if agent is already running
if curl -s http://localhost:7777/api/status &> /dev/null; then
    echo -e "${GREEN}✅ ZTM Agent is already running${NC}"
else
    echo -e "${BLUE}   Starting ZTM Agent on localhost:7777...${NC}"
    
    # Start agent in background
    ztm start agent
    
    # Wait for agent to be ready
    echo -e "${BLUE}   Waiting for agent to be ready...${NC}"
    for i in {1..30}; do
        if curl -s http://localhost:7777/api/status &> /dev/null; then
            echo -e "${GREEN}✅ ZTM Agent is ready!${NC}"
            break
        fi
        sleep 1
    done
    
    if ! curl -s http://localhost:7777/api/status &> /dev/null; then
        echo -e "${RED}❌ Failed to start ZTM Agent${NC}"
        exit 1
    fi
fi

echo -e "${YELLOW}📱 Step 4: Checking Tunnel App...${NC}"

# Install tunnel app if not already installed
ztm get app 2>/dev/null | grep -q "ztm/tunnel"
if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✅ Tunnel app is already installed${NC}"
else
    echo -e "${BLUE}   Installing tunnel app...${NC}"
    ztm app install tunnel
    echo -e "${GREEN}✅ Tunnel app installed!${NC}"
fi

echo -e "${YELLOW}⚙️  Step 5: Configuration...${NC}"

# Create default config if not exists
ZTM_CONF="$HOME/.ztm.conf"
if [[ ! -f "$ZTM_CONF" ]]; then
    echo -e "${BLUE}   Creating default config at $ZTM_CONF${NC}"
    cat > "$ZTM_CONF" << 'EOF'
{
  "agent": "localhost:7777",
  "mesh": ""
}
EOF
    echo -e "${GREEN}✅ Default config created${NC}"
else
    echo -e "${BLUE}   Config already exists at $ZTM_CONF${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Join a mesh network (if not already joined):"
echo "     ztm join <mesh-name> --as <your-name> --permit <permit-file.json>"
echo ""
echo "  2. List tunnels:"
echo "     ztm tunnel get tunnel"
echo ""
echo "  3. Create a tunnel:"
echo "     ztm tunnel open outbound my-tunnel --targets 192.168.1.100:8080"
echo "     ztm tunnel open inbound my-tunnel --listen 0.0.0.0:9000 --exits <endpoint-id>"
echo ""
echo "For more commands, see: ztm help"
