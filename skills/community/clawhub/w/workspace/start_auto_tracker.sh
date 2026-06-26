#!/bin/bash
# Start Jira Auto Tracker as a background service

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/jira_auto_tracker.py"
PID_FILE="$SCRIPT_DIR/.auto_tracker.pid"
LOG_FILE="$SCRIPT_DIR/jira_tracker.log"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

start_tracker() {
    if check_pid; then
        echo -e "${YELLOW}⚠️  Auto Tracker is already running${NC}"
        echo "  PID: $(cat "$PID_FILE")"
        echo "  Logs: $LOG_FILE"
        exit 1
    fi
    
    echo -e "${GREEN}🚀 Starting Jira Auto Tracker${NC}"
    echo "   This will run continuously in the background"
    echo "   Work hours: 8:00 - 19:00 (Tehran time, Mon-Fri)"
    echo "   Prompts at: 09:30, 12:00, 15:30, 17:00, 18:30"
    echo "   Log file: $LOG_FILE"
    echo ""
    
    # Start in background
    nohup python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1 &
    
    PID=$!
    echo $PID > "$PID_FILE"
    
    sleep 2  # Give it time to start
    
    if check_pid; then
        echo -e "${GREEN}✅ Auto Tracker started successfully${NC}"
        echo "   PID: $PID"
        echo "   To stop: $0 stop"
        echo "   To check status: $0 status"
        echo "   To view logs: tail -f '$LOG_FILE'"
        echo ""
        echo -e "${BLUE}📋 What happens now:${NC}"
        echo "   • Runs continuously (even if terminal closes)"
        echo "   • Creates daily log at 8:00 AM"
        echo "   • Sends notifications at scheduled times"
        echo "   • Random reminders during work hours"
        echo "   • Uses macOS notifications"
    else
        echo -e "${RED}❌ Failed to start Auto Tracker${NC}"
        echo "   Check logs: $LOG_FILE"
        rm -f "$PID_FILE"
        exit 1
    fi
}

stop_tracker() {
    if check_pid; then
        PID=$(cat "$PID_FILE")
        echo -e "${YELLOW}🛑 Stopping Auto Tracker (PID: $PID)...${NC}"
        kill "$PID"
        sleep 3
        
        if kill -0 "$PID" 2>/dev/null; then
            echo -e "${RED}❌ Failed to stop, forcing...${NC}"
            kill -9 "$PID"
        fi
        
        rm -f "$PID_FILE"
        echo -e "${GREEN}✅ Auto Tracker stopped${NC}"
    else
        echo -e "${YELLOW}⚠️  Auto Tracker is not running${NC}"
    fi
}

show_status() {
    if check_pid; then
        PID=$(cat "$PID_FILE")
        echo -e "${GREEN}✅ Auto Tracker is running${NC}"
        echo "  PID: $PID"
        echo "  Started: $(ps -p "$PID" -o lstart= 2>/dev/null || echo "Unknown")"
        echo "  Memory: $(ps -p "$PID" -o rss= 2>/dev/null | awk '{printf "%.1f MB", $1/1024}')"
        echo "  CPU: $(ps -p "$PID" -o %cpu= 2>/dev/null || echo "Unknown")%"
        
        # Show log file size
        if [[ -f "$LOG_FILE" ]]; then
            echo "  Log size: $(wc -l < "$LOG_FILE" | awk '{print $1}') lines"
        fi
        
        echo ""
        echo -e "${BLUE}Recent log output:${NC}"
        tail -10 "$LOG_FILE" 2>/dev/null | while IFS= read -r line; do
            echo "  $line"
        done
    else
        echo -e "${YELLOW}⚠️  Auto Tracker is not running${NC}"
    fi
}

show_help() {
    echo -e "${BLUE}Jira Auto Tracker - Background Service${NC}"
    echo "Runs continuously to prompt for Jira work logging"
    echo ""
    echo "Usage:"
    echo "  $0 start      Start the auto tracker (background)"
    echo "  $0 stop       Stop the auto tracker"
    echo "  $0 status     Check status and view logs"
    echo "  $0 restart    Restart the auto tracker"
    echo "  $0 logs       View recent logs"
    echo "  $0 --help     Show this help"
    echo ""
    echo "Features:"
    echo "  • Runs 24/7 in background"
    echo "  • Auto-starts daily log at 8:00 AM"
    echo "  • Scheduled prompts throughout day"
    echo "  • Random reminders during work hours"
    echo "  • macOS notifications"
    echo "  • No manual commands needed"
    echo ""
    echo "Schedule:"
    echo "  08:00-08:30  Create daily log"
    echo "  09:30        Morning reminder"
    echo "  12:00        Mid-day check"
    echo "  15:30        Afternoon check"
    echo "  17:00        End of day approaching"
    echo "  18:30        Final reminder"
}

case "$1" in
    start)
        start_tracker
        ;;
    stop)
        stop_tracker
        ;;
    status)
        show_status
        ;;
    restart)
        stop_tracker
        sleep 2
        start_tracker
        ;;
    logs)
        if [[ -f "$LOG_FILE" ]]; then
            tail -50 "$LOG_FILE"
        else
            echo "No log file found"
        fi
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