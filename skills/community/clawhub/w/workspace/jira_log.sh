#!/bin/bash
# Jira Work Log Helper Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/jira_tools.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

help_text() {
    echo -e "${BLUE}Jira Work Log Helper${NC}"
    echo ""
    echo "Usage:"
    echo "  $0 test                   Test Jira connection"
    echo "  $0 list                   List your recent/issues"
    echo "  $0 log                    Quick log work (interactive)"
    echo "  $0 today                  Show today's work log template"
    echo "  $0 reminder               Set up reminders for logging"
    echo "  $0 --help                 Show this help"
    echo ""
    echo "Advanced:"
    echo "  $0 log --issue PROJ-123 --time '1h 30m' --comment 'My work'"
    echo ""
}

case "$1" in
    test)
        python3 "$PYTHON_SCRIPT" test
        ;;
    list)
        python3 "$PYTHON_SCRIPT" list
        ;;
    log)
        if [[ -n "$2" && "$2" != "--"* ]]; then
            # Direct log with arguments
            python3 "$PYTHON_SCRIPT" log --issue "$2" --time "$3" --comment "$4"
        else
            # Interactive mode
            python3 "$PYTHON_SCRIPT" quick
        fi
        ;;
    today)
        # Show today's work log template
        TODAY=$(date +%Y-%m-%d)
        echo -e "${GREEN}📅 Today's Work Log Template ($TODAY)${NC}"
        echo "=========================================="
        echo ""
        echo "# Jira Work Log - $TODAY"
        echo ""
        echo "## Morning (9:00-12:00)"
        echo "- [ ] "
        echo "- [ ] "
        echo ""
        echo "## Afternoon (13:00-17:00)"
        echo "- [ ] "
        echo "- [ ] "
        echo ""
        echo "## Time Summary"
        echo "- Total time: "
        echo "- Issues worked on: "
        echo ""
        echo "## Notes"
        echo ""
        echo ""
        echo "To log work:"
        echo "  ./jira_log.sh log"
        echo ""
        ;;
    reminder)
        echo -e "${YELLOW}Setting up reminders...${NC}"
        
        # Check if remindctl is available
        if command -v remindctl &> /dev/null; then
            echo "Using Apple Reminders to set up daily reminders..."
            
            # Remove existing Jira reminders if any
            remindctl delete "Jira: Log morning work" 2>/dev/null || true
            remindctl delete "Jira: Log afternoon work" 2>/dev/null || true
            remindctl delete "Jira: End of day summary" 2>/dev/null || true
            
            # Create new reminders
            remindctl add "Jira: Log morning work" --due "today 12:00" --repeat daily
            remindctl add "Jira: Log afternoon work" --due "today 17:00" --repeat daily
            remindctl add "Jira: End of day summary" --due "today 18:00" --repeat daily
            
            echo -e "${GREEN}✅ Reminders set!${NC}"
            echo "   - 12:00: Log morning work"
            echo "   - 17:00: Log afternoon work"
            echo "   - 18:00: End of day summary"
        else
            echo -e "${RED}❌ remindctl not found. Install it with:${NC}"
            echo "   npm install -g @openclaw/remindctl"
            echo ""
            echo "Alternative: Use macOS Calendar or set alarms manually."
        fi
        ;;
    --help|-h)
        help_text
        ;;
    *)
        if [[ -z "$1" ]]; then
            help_text
        else
            echo -e "${RED}Unknown command: $1${NC}"
            help_text
            exit 1
        fi
        ;;
esac