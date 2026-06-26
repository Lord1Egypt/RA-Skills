#!/bin/bash
# Setup Manual Work Prompt System

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Manual Work Prompt System Setup     ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check prerequisites
echo "🧪 Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✅ Python3 found${NC}"
else
    echo -e "${YELLOW}❌ Python3 not found${NC}"
    exit 1
fi

# Check requests library
if python3 -c "import requests" 2>/dev/null; then
    echo -e "${GREEN}✅ requests library found${NC}"
else
    echo -e "${YELLOW}⚠️  requests library not found${NC}"
    echo "Installing requests library..."
    python3 -m pip install requests --proxy http://localhost:2080 --user --break-system-packages
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ requests library installed${NC}"
    else
        echo -e "${YELLOW}❌ Failed to install requests${NC}"
        exit 1
    fi
fi

# Check Jira config
if [[ -f "jira_config.json" ]]; then
    echo -e "${GREEN}✅ jira_config.json found${NC}"
    
    # Test Jira connection
    echo "Testing Jira connection..."
    python3 -c "
from jira_tools import JiraClient
jira = JiraClient()
if jira.test_connection():
    print('✅ Jira connection successful')
else:
    print('❌ Jira connection failed')
    exit(1)
"
else
    echo -e "${YELLOW}⚠️  jira_config.json not found${NC}"
    echo "Please create jira_config.json first:"
    echo "  cp jira_config.example.json jira_config.json"
    echo "  nano jira_config.json"
    exit 1
fi

# Make scripts executable
echo ""
echo "🔧 Setting up scripts..."
chmod +x *.sh 2>/dev/null
chmod +x *.py 2>/dev/null
echo -e "${GREEN}✅ Scripts made executable${NC}"

# Create daily logs directory
mkdir -p daily_logs
echo -e "${GREEN}✅ Created daily_logs directory${NC}"

# Show system overview
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   System Overview                     ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}✅ INSTALLATION COMPLETE${NC}"
echo ""
echo "📋 Available Commands:"
echo "  ./start_prompts.sh start     - Start prompt system"
echo "  ./start_prompts.sh stop      - Stop prompt system"
echo "  ./start_prompts.sh status    - Check status"
echo "  ./start_prompts.sh test      - Test notifications"
echo "  ./jira_log.sh log            - Log work to Jira"
echo "  ./create_daily_log.sh        - Create daily log"
echo ""
echo "⏰ Work Hours: 8:00 - 19:00 (Tehran time)"
echo "🔔 Scheduled Prompts:"
echo "  12:00 - Mid-day check"
echo "  16:00 - Afternoon check"
echo "  18:30 - End of day"
echo ""
echo "📊 Resource Usage:"
echo "  • CPU: < 1% when idle"
echo "  • Memory: ~30 MB"
echo "  • Storage: ~100 KB"
echo "  • Network: Only Jira API calls"
echo ""
echo "🔒 Privacy:"
echo "  • No activity monitoring"
echo "  • No external services"
echo "  • Only Jira API communication"
echo ""
echo -e "${BLUE}========================================${NC}"
echo "To start the system:"
echo -e "  ${GREEN}./start_prompts.sh start${NC}"
echo ""
echo "To run in background (recommended):"
echo -e "  ${GREEN}nohup ./start_prompts.sh start &${NC}"
echo -e "${BLUE}========================================${NC}"