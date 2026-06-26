#!/bin/bash
echo "🧪 Testing Jira Work Log Setup"
echo "================================"

# Check if jira_config.json exists
if [[ -f "jira_config.json" ]]; then
    echo "✅ jira_config.json exists"
    echo "   Please edit it with your credentials:"
    echo "   - username: Your Jira username/email"
    echo "   - api_token: Your API token from https://id.atlassian.com/manage/api-tokens"
    echo "   - jira_url: https://jira.neor.space"
    echo "   - default_project: Your project key"
else
    echo "❌ jira_config.json missing"
    echo "   Run: cp jira_config.example.json jira_config.json"
    exit 1
fi

# Check Python
echo ""
echo "🐍 Checking Python..."
python3 --version
if command -v python3 &> /dev/null; then
    echo "✅ Python3 found"
else
    echo "❌ Python3 not found"
    exit 1
fi

# Check requests library
echo ""
echo "📦 Checking Python dependencies..."
python3 -c "import requests; print('✅ requests library:', requests.__version__)"
if [[ $? -eq 0 ]]; then
    echo "✅ requests library installed"
else
    echo "❌ requests library not installed"
    echo "   Install with: python3 -m pip install requests --proxy http://localhost:2080 --user --break-system-packages"
    exit 1
fi

# Check scripts
echo ""
echo "📜 Checking scripts..."
if [[ -f "jira_tools.py" && -x "jira_log.sh" ]]; then
    echo "✅ All scripts present and executable"
else
    echo "❌ Scripts missing or not executable"
    echo "   Run: chmod +x *.sh"
    exit 1
fi

echo ""
echo "🎉 Setup looks good!"
echo ""
echo "Next steps:"
echo "1. Edit jira_config.json with your credentials"
echo "2. Test connection: ./jira_log.sh test"
echo "3. Try logging work: ./jira_log.sh log"
echo ""
echo "Optional:"
echo "- Set up reminders: ./jira_log.sh reminder"
echo "- Create daily log: ./create_daily_log.sh"