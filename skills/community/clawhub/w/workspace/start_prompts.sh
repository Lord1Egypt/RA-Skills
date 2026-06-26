#!/bin/bash
# Manual Work Prompt System Launcher
# Time-based reminders for Jira work logging

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/work_prompt_system.py"
PID_FILE="$SCRIPT_DIR/.prompt_system.pid"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_help() {
    echo -e "${BLUE}Manual Work Prompt System${NC}"
    echo "Time-based reminders for Jira work logging (8 AM - 7 PM)"
    echo ""
    echo "Usage:"
    echo "  $0 start [--interval MINUTES]    Start the prompt system"
    echo "  $0 stop                          Stop the prompt system"
    echo "  $0 status                        Check if system is running"
    echo "  $0 test                          Test notifications and Jira connection"
    echo "  $0 log                           Quick Jira work log"
    echo "  $0 today                         Create today's daily log"
    echo "  $0 --help                        Show this help"
    echo ""
    echo "Options:"
    echo "  --interval MINUTES  Check interval (default: 30 minutes)"
    echo ""
    echo "Features:"
    echo "  • Scheduled prompts at 12:00, 16:00, 18:30"
    echo "  • Random reminders during work hours"
    echo "  • macOS notifications"
    echo "  • No activity monitoring"
    echo "  • Minimal resource usage"
}

check_pid() {
    if [[ -f "$PID_FILE" ]]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            return 0  # Running
        else
            rm -f "$PID_FILE"
            return 1  # Not running
        fi
    else
        return 1  # Not running
    fi
}

start_system() {
    INTERVAL=30
    
    # Parse interval argument
    while [[ $# -gt 0 ]]; do
        case $1 in
            --interval)
                INTERVAL="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done
    
    if check_pid; then
        echo -e "${YELLOW}⚠️  Prompt system is already running${NC}"
        echo "  PID: $(cat "$PID_FILE")"
        exit 1
    fi
    
    echo -e "${GREEN}🚀 Starting Manual Work Prompt System${NC}"
    echo "   Interval: ${INTERVAL} minutes"
    echo "   Work hours: 8:00 - 19:00 (Tehran time)"
    echo "   Scheduled prompts: 12:00, 16:00, 18:30"
    echo ""
    echo "Log file: $SCRIPT_DIR/prompt_system.log"
    echo ""
    
    # Start in background and log to file
    nohup python3 "$PYTHON_SCRIPT" start --interval "$INTERVAL" > "$SCRIPT_DIR/prompt_system.log" 2>&1 &
    
    PID=$!
    echo $PID > "$PID_FILE"
    
    echo -e "${GREEN}✅ Prompt system started (PID: $PID)${NC}"
    echo "   To stop: $0 stop"
    echo "   To check status: $0 status"
    echo "   To view logs: tail -f '$SCRIPT_DIR/prompt_system.log'"
}

stop_system() {
    if check_pid; then
        PID=$(cat "$PID_FILE")
        echo -e "${YELLOW}🛑 Stopping prompt system (PID: $PID)...${NC}"
        kill "$PID"
        sleep 2
        
        if kill -0 "$PID" 2>/dev/null; then
            echo -e "${RED}❌ Failed to stop, forcing...${NC}"
            kill -9 "$PID"
        fi
        
        rm -f "$PID_FILE"
        echo -e "${GREEN}✅ Prompt system stopped${NC}"
    else
        echo -e "${YELLOW}⚠️  Prompt system is not running${NC}"
    fi
}

show_status() {
    if check_pid; then
        PID=$(cat "$PID_FILE")
        echo -e "${GREEN}✅ Prompt system is running${NC}"
        echo "  PID: $PID"
        echo "  Started: $(ps -p "$PID" -o lstart= 2>/dev/null || echo "Unknown")"
        echo "  Memory: $(ps -p "$PID" -o rss= 2>/dev/null | awk '{printf "%.1f MB", $1/1024}')"
        
        # Show recent log
        echo ""
        echo -e "${BLUE}Recent log output:${NC}"
        tail -5 "$SCRIPT_DIR/prompt_system.log" 2>/dev/null || echo "No log file found"
    else
        echo -e "${YELLOW}⚠️  Prompt system is not running${NC}"
    fi
}

case "$1" in
    start)
        shift
        start_system "$@"
        ;;
    stop)
        stop_system
        ;;
    status)
        show_status
        ;;
    test)
        echo -e "${BLUE}🧪 Testing system...${NC}"
        python3 "$PYTHON_SCRIPT" test
        ;;
    log)
        echo -e "${BLUE}📝 Quick Jira work log...${NC}"
        python3 "$PYTHON_SCRIPT" log
        ;;
    today)
        echo -e "${BLUE}📅 Creating today's log...${NC}"
        python3 "$PYTHON_SCRIPT" today
        ;;
    --help|-h)
        show_help
        ;;
    *)
        if [[ -z "$1" ]]; then
            show_help
        else
            echo -e "${RED}❌ Unknown command: $1${NC}"
            show_help
            exit 1
        fi
        ;;
esac