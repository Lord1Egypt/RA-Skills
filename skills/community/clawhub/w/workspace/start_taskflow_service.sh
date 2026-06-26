#!/bin/bash
# Start Jira TaskFlow Service
# This survives session timeouts and runs independently

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/jira_taskflow.py"
PID_FILE="$SCRIPT_DIR/.taskflow_service.pid"
LOG_FILE="$SCRIPT_DIR/taskflow_service.log"
STATE_FILE="$SCRIPT_DIR/.jira_taskflow_state.json"

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

start_service() {
    if check_pid; then
        echo -e "${YELLOW}⚠️  TaskFlow Service is already running${NC}"
        echo "  PID: $(cat "$PID_FILE")"
        echo "  Logs: $LOG_FILE"
        exit 1
    fi
    
    echo -e "${GREEN}🚀 Starting Jira TaskFlow Service${NC}"
    echo "   This service survives session timeouts"
    echo "   Work hours: 8:00 - 19:00 (Tehran time, Mon-Fri)"
    echo "   State file: $STATE_FILE"
    echo "   Log file: $LOG_FILE"
    echo ""
    echo -e "${BLUE}📅 Daily Schedule:${NC}"
    echo "   08:00  Create daily log automatically"
    echo "   09:00  Health check"
    echo "   09:30  Morning reminder"
    echo "   12:00  Mid-day check"
    echo "   15:30  Afternoon check"
    echo "   17:00  End of day approaching"
    echo "   18:30  Final reminder"
    echo ""
    
    # Start in background with nohup
    nohup python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1 &
    
    PID=$!
    echo $PID > "$PID_FILE"
    
    sleep 3  # Give it time to start
    
    if check_pid; then
        echo -e "${GREEN}✅ TaskFlow Service started successfully${NC}"
        echo "   PID: $PID"
        echo "   To stop: $0 stop"
        echo "   To check status: $0 status"
        echo "   To view logs: tail -f '$LOG_FILE'"
        echo ""
        echo -e "${BLUE}🎯 Key Features:${NC}"
        echo "   • Survives API timeouts"
        echo "   • Persistent state between runs"
        echo "   • No manual intervention needed"
        echo "   • Auto-recovers from crashes"
    else
        echo -e "${RED}❌ Failed to start TaskFlow Service${NC}"
        echo "   Check logs: $LOG_FILE"
        rm -f "$PID_FILE"
        exit 1
    fi
}

stop_service() {
    if check_pid; then
        PID=$(cat "$PID_FILE")
        echo -e "${YELLOW}🛑 Stopping TaskFlow Service (PID: $PID)...${NC}"
        kill "$PID"
        sleep 3
        
        if kill -0 "$PID" 2>/dev/null; then
            echo -e "${RED}❌ Failed to stop, forcing...${NC}"
            kill -9 "$PID"
        fi
        
        rm -f "$PID_FILE"
        echo -e "${GREEN}✅ TaskFlow Service stopped${NC}"
    else
        echo -e "${YELLOW}⚠️  TaskFlow Service is not running${NC}"
    fi
}

show_status() {
    if check_pid; then
        PID=$(cat "$PID_FILE")
        echo -e "${GREEN}✅ TaskFlow Service is running${NC}"
        echo "  PID: $PID"
        echo "  Started: $(ps -p "$PID" -o lstart= 2>/dev/null || echo "Unknown")"
        echo "  Memory: $(ps -p "$PID" -o rss= 2>/dev/null | awk '{printf "%.1f MB", $1/1024}')"
        echo "  CPU: $(ps -p "$PID" -o %cpu= 2>/dev/null || echo "Unknown")%"
        
        # Show state info
        if [[ -f "$STATE_FILE" ]]; then
            echo "  State: $(jq -r '.last_daily_log // "Never"' "$STATE_FILE" 2>/dev/null || echo "Unknown")"
        fi
        
        # Show log file info
        if [[ -f "$LOG_FILE" ]]; then
            echo "  Log size: $(wc -l < "$LOG_FILE" | awk '{print $1}') lines"
            echo "  Last log: $(tail -1 "$LOG_FILE" 2>/dev/null | cut -c1-80)"
        fi
        
        echo ""
        echo -e "${BLUE}Recent activity:${NC}"
        tail -5 "$LOG_FILE" 2>/dev/null | while IFS= read -r line; do
            echo "  $line"
        done
    else
        echo -e "${YELLOW}⚠️  TaskFlow Service is not running${NC}"
    fi
}

show_help() {
    echo -e "${BLUE}Jira TaskFlow Service - Session-Timeout Proof${NC}"
    echo "Persistent background service for Jira work log management"
    echo ""
    echo "Usage:"
    echo "  $0 start      Start the persistent service"
    echo "  $0 stop       Stop the service"
    echo "  $0 status     Check status and view state"
    echo "  $0 restart    Restart the service"
    echo "  $0 logs       View recent logs"
    echo "  $0 state      View current state"
    echo "  $0 --help     Show this help"
    echo ""
    echo "Features:"
    echo "  • Survives API/session timeouts"
    echo "  • Persistent state between runs"
    echo "  • Auto-scheduled tasks"
    echo "  • Health monitoring"
    echo "  • Crash recovery"
    echo ""
    echo "Designed for OpenClaw with timeout-limited model APIs"
}

case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    status)
        show_status
        ;;
    restart)
        stop_service
        sleep 2
        start_service
        ;;
    logs)
        if [[ -f "$LOG_FILE" ]]; then
            tail -50 "$LOG_FILE"
        else
            echo "No log file found"
        fi
        ;;
    state)
        if [[ -f "$STATE_FILE" ]]; then
            jq . "$STATE_FILE" 2>/dev/null || cat "$STATE_FILE"
        else
            echo "No state file found"
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