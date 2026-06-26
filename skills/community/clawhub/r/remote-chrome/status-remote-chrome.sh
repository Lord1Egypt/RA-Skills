#!/bin/bash
# Monitor Chrome Remote Access Service Status

# Configuration parameters (must match start script)
DISPLAY_NUM=99
VNC_PORT=5900
NOVNC_PORT=6080
CHROME_DEBUG_PORT=9222
CHROME_BIN="chromium"  # Can be changed to google-chrome-stable

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --vnc-port)
            if [ -n "$2" ] && [[ "$2" != -* ]]; then
                VNC_PORT="$2"
                shift 2
            else
                echo -e "${RED}✗ Error: --vnc-port requires a port number${NC}"
                exit 1
            fi
            ;;
        --novnc-port)
            if [ -n "$2" ] && [[ "$2" != -* ]]; then
                NOVNC_PORT="$2"
                shift 2
            else
                echo -e "${RED}✗ Error: --novnc-port requires a port number${NC}"
                exit 1
            fi
            ;;
        --chrome-debug-port)
            if [ -n "$2" ] && [[ "$2" != -* ]]; then
                CHROME_DEBUG_PORT="$2"
                shift 2
            else
                echo -e "${RED}✗ Error: --chrome-debug-port requires a port number${NC}"
                exit 1
            fi
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --vnc-port <port>            VNC server port (default: 5900)"
            echo "  --novnc-port <port>          noVNC web access port (default: 6080)"
            echo "  --chrome-debug-port <port>   Chrome remote debugging port (default: 9222)"
            echo "  -h, --help                   Display help information"
            echo ""
            echo "Note: Port options must match the ports used when starting the service"
            exit 0
            ;;
        *)
            echo -e "${RED}✗ Error: Unknown parameter $1${NC}"
            echo "Use -h or --help to view help"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║   Remote Chrome Service Status Monitor     ║${NC}"
echo -e "${GREEN}${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""

# Find Chrome/Chromium executable
find_chrome() {
    for bin in chromium chromium-browser google-chrome-stable google-chrome; do
        if which $bin >/dev/null 2>&1; then
            echo $bin
            return
        fi
    done
    return 1
}

# Format memory size
format_memory() {
    local kb=$1
    if [ $kb -ge 1048576 ]; then
        echo "$(echo "scale=1; $kb/1048576" | bc) GB"
    elif [ $kb -ge 1024 ]; then
        echo "$(echo "scale=1; $kb/1024" | bc) MB"
    else
        echo "${kb} KB"
    fi
}

# Get process memory usage
get_process_memory() {
    local pid=$1
    if [ -n "$pid" ]; then
        local mem_kb=$(ps -p $pid -o rss= 2>/dev/null | tr -d ' ')
        if [ -n "$mem_kb" ] && [ "$mem_kb" -gt 0 ] 2>/dev/null; then
            format_memory $mem_kb
        else
            echo "N/A"
        fi
    else
        echo "N/A"
    fi
}

# Get Chrome tab information
get_chrome_tabs() {
    if command -v curl >/dev/null 2>&1 && command -v jq >/dev/null 2>&1; then
        local tabs_json=$(curl -s http://localhost:${CHROME_DEBUG_PORT}/json 2>/dev/null)
        if [ -n "$tabs_json" ]; then
            echo "$tabs_json"
        fi
    elif command -v curl >/dev/null 2>&1; then
        # No jq, return raw JSON
        curl -s http://localhost:${CHROME_DEBUG_PORT}/json 2>/dev/null
    fi
}

# Auto-detect Chrome/Chromium
if ! which $CHROME_BIN >/dev/null 2>&1; then
    CHROME_BIN=$(find_chrome)
fi

# Check process status
XVFB_PID=$(pgrep -f "Xvfb :${DISPLAY_NUM}" | head -1)
X11VNC_PID=$(pgrep -f "x11vnc.*:${DISPLAY_NUM}" | head -1)
WEBSOCKIFY_PID=$(pgrep -f "websockify.*${NOVNC_PORT}" | head -1)

# Find Chrome main process (prioritize finding process with debug port)
CHROME_PID=""
if command -v lsof >/dev/null 2>&1; then
    # Find via debug port
    CHROME_PID=$(lsof -ti:${CHROME_DEBUG_PORT} 2>/dev/null | head -1)
fi

# If not found, try to find via process name and environment variable
if [ -z "$CHROME_PID" ] && command -v pgrep >/dev/null 2>&1; then
    for pid in $(pgrep -f "${CHROME_BIN}" | head -20); do
        # Skip child processes (type=xxx processes)
        if [ -r /proc/$pid/cmdline ]; then
            CMD=$(tr '\0' ' ' < /proc/$pid/cmdline)
            if echo "$CMD" | grep -q "remote-debugging-port=${CHROME_DEBUG_PORT}" 2>/dev/null; then
                CHROME_PID=$pid
                break
            fi
        fi

        # Check DISPLAY environment variable
        if [ -r /proc/$pid/environ ]; then
            if grep -q "DISPLAY=:${DISPLAY_NUM}" /proc/$pid/environ 2>/dev/null; then
                # Ensure it's not a child process
                if [ -r /proc/$pid/cmdline ]; then
                    CMD=$(tr '\0' ' ' < /proc/$pid/cmdline)
                    if ! echo "$CMD" | grep -q "type=" 2>/dev/null; then
                        CHROME_PID=$pid
                        break
                    fi
                fi
            fi
        fi
    done
fi

# Check if service is running
SERVICE_RUNNING=false
if [ -n "$XVFB_PID" ] && [ -n "$X11VNC_PID" ] && [ -n "$WEBSOCKIFY_PID" ]; then
    SERVICE_RUNNING=true
fi

if [ "$SERVICE_RUNNING" = true ]; then
    echo -e "${GREEN}${BOLD}📊 Service Status: Running${NC}"
    echo ""

    # Process information and memory usage
    echo -e "${BOLD}Process Information:${NC}"

    if [ -n "$XVFB_PID" ]; then
        XVFB_MEM=$(get_process_memory $XVFB_PID)
        echo -e "  ${GREEN}✓${NC} Xvfb (PID: ${XVFB_PID}) - Memory: ${CYAN}${XVFB_MEM}${NC}"
    else
        echo -e "  ${RED}✗${NC} Xvfb not running"
    fi

    if [ -n "$X11VNC_PID" ]; then
        X11VNC_MEM=$(get_process_memory $X11VNC_PID)
        echo -e "  ${GREEN}✓${NC} x11vnc (PID: ${X11VNC_PID}) - Memory: ${CYAN}${X11VNC_MEM}${NC}"
    else
        echo -e "  ${RED}✗${NC} x11vnc not running"
    fi

    if [ -n "$WEBSOCKIFY_PID" ]; then
        WS_MEM=$(get_process_memory $WEBSOCKIFY_PID)
        echo -e "  ${GREEN}✓${NC} noVNC/websockify (PID: ${WEBSOCKIFY_PID}) - Memory: ${CYAN}${WS_MEM}${NC}"
    else
        echo -e "  ${RED}✗${NC} noVNC not running"
    fi

    if [ -n "$CHROME_PID" ]; then
        CHROME_MEM=$(get_process_memory $CHROME_PID)
        echo -e "  ${GREEN}✓${NC} Chrome (PID: ${CHROME_PID}) - Memory: ${CYAN}${CHROME_MEM}${NC}"

        # Get total memory of all Chrome related processes
        TOTAL_CHROME_MEM=0
        for cpid in $(pgrep -f "${CHROME_BIN}"); do
            CMEM=$(ps -p $cpid -o rss= 2>/dev/null | tr -d ' ')
            if [ -n "$CMEM" ] && [ "$CMEM" -gt 0 ] 2>/dev/null; then
                TOTAL_CHROME_MEM=$((TOTAL_CHROME_MEM + CMEM))
            fi
        done

        if [ "$TOTAL_CHROME_MEM" -gt 0 ] 2>/dev/null; then
            TOTAL_FORMATTED=$(format_memory $TOTAL_CHROME_MEM)
            echo -e "    ${YELLOW}→ Total Chrome processes memory: ${CYAN}${TOTAL_FORMATTED}${NC}"
        fi
    else
        echo -e "  ${YELLOW}⚠${NC} Chrome not running (optional)"
    fi

    # Port and address information
    echo ""
    echo -e "${BOLD}Ports and Addresses:${NC}"

    # VNC port
    if ss -tuln 2>/dev/null | grep -q ":${VNC_PORT} " || netstat -tuln 2>/dev/null | grep -q ":${VNC_PORT} "; then
        VNC_ADDR=$(ss -tuln 2>/dev/null | grep ":${VNC_PORT} " | head -1 | awk '{print $5}' || netstat -tuln 2>/dev/null | grep ":${VNC_PORT} " | head -1 | awk '{print $4}')
        echo -e "  ${GREEN}✓${NC} VNC: ${CYAN}${VNC_ADDR}${NC}"
    else
        echo -e "  ${RED}✗${NC} VNC port ${VNC_PORT} not listening"
    fi

    # noVNC port
    if ss -tuln 2>/dev/null | grep -q ":${NOVNC_PORT} " || netstat -tuln 2>/dev/null | grep -q ":${NOVNC_PORT} "; then
        NOVNC_ADDR=$(ss -tuln 2>/dev/null | grep ":${NOVNC_PORT} " | head -1 | awk '{print $5}' || netstat -tuln 2>/dev/null | grep ":${NOVNC_PORT} " | head -1 | awk '{print $4}')
        echo -e "  ${GREEN}✓${NC} noVNC: ${CYAN}${NOVNC_ADDR}${NC}"
    else
        echo -e "  ${RED}✗${NC} noVNC port ${NOVNC_PORT} not listening"
    fi

    # Chrome debug port
    if ss -tuln 2>/dev/null | grep -q ":${CHROME_DEBUG_PORT} " || netstat -tuln 2>/dev/null | grep -q ":${CHROME_DEBUG_PORT} "; then
        DEBUG_ADDR=$(ss -tuln 2>/dev/null | grep ":${CHROME_DEBUG_PORT} " | head -1 | awk '{print $5}' || netstat -tuln 2>/dev/null | grep ":${CHROME_DEBUG_PORT} " | head -1 | awk '{print $4}')
        echo -e "  ${GREEN}✓${NC} Chrome Debug: ${CYAN}${DEBUG_ADDR}${NC}"
    fi

    # Get host IP
    HOST_IP=$(hostname -I | awk '{print $1}')
    HOSTNAME=$(hostname | cut -d'.' -f1)

    # Get VNC password from password file
    VNC_PASSWORD=""
    if [ -f /tmp/remote-chrome-vnc-password.txt ]; then
        VNC_PASSWORD=$(cat /tmp/remote-chrome-vnc-password.txt 2>/dev/null)
    fi

    # Display access information
    echo ""
    echo -e "${GREEN}${BOLD}═════════════════════════════════════════════${NC}"
    echo -e "${GREEN}${BOLD}          Access Information${NC}"
    echo -e "${GREEN}${BOLD}═════════════════════════════════════════════${NC}"
    echo ""

    if [ -n "$VNC_PASSWORD" ]; then
        echo -e "${BOLD}📱 Web Access URL (Recommended):${NC}"
        echo -e "   ${CYAN}${BOLD}http://${HOST_IP}:${NOVNC_PORT}/vnc.html?host=${HOST_IP}&port=${NOVNC_PORT}&password=${VNC_PASSWORD}&autoconnect=true${NC}"
        echo ""
        echo -e "${BOLD}💻 VNC Client Connection:${NC}"
        echo -e "   ${CYAN}${BOLD}${HOST_IP}:${VNC_PORT}${NC} ${YELLOW}(Password: ${VNC_PASSWORD})${NC}"
        echo ""
        echo -e "${BOLD}🔑 VNC Password: ${CYAN}${BOLD}${VNC_PASSWORD}${NC}"
    else
        echo -e "${YELLOW}⚠ VNC password not found, may need to check startup logs${NC}"
        echo ""
        echo -e "${BOLD}📱 Web Access URL:${NC}"
        echo -e "   ${CYAN}${BOLD}http://${HOST_IP}:${NOVNC_PORT}/vnc.html${NC}"
        echo ""
        echo -e "${BOLD}💻 VNC Client Connection:${NC}"
        echo -e "   ${CYAN}${BOLD}${HOST_IP}:${VNC_PORT}${NC}"
    fi

    # Chrome remote debug port
    if [ -n "$CHROME_PID" ]; then
        echo ""
        echo -e "${BOLD}🔧 Chrome Remote Debugging:${NC}"
        echo -e "   ${CYAN}${BOLD}http://${HOST_IP}:${CHROME_DEBUG_PORT}${NC}"

        # Get and display Chrome tab information
        echo ""
        echo -e "${BOLD}📑 Chrome Tabs:${NC}"
        TABS_INFO=$(get_chrome_tabs)
        if [ -n "$TABS_INFO" ]; then
            if command -v jq >/dev/null 2>&1; then
                # Use jq to parse JSON
                TAB_COUNT=$(echo "$TABS_INFO" | jq -r 'length' 2>/dev/null)
                if [ -n "$TAB_COUNT" ] && [ "$TAB_COUNT" -gt 0 ] 2>/dev/null; then
                    echo -e "  ${CYAN}Total ${TAB_COUNT} tabs${NC}"
                    echo ""

                    # Display each tab's information
                    echo "$TABS_INFO" | jq -r '.[] | "\(.type)\t\(.title)\t\(.url)"' 2>/dev/null | head -10 | while IFS=$'\t' read -r type title url; do
                        if [ -n "$title" ] && [ "$type" = "page" ]; then
                            # Truncate long titles
                            if [ ${#title} -gt 50 ]; then
                                title="${title:0:47}..."
                            fi
                            echo -e "  ${GREEN}•${NC} ${title}"
                            if [ ${#url} -gt 60 ]; then
                                url="${url:0:57}..."
                            fi
                            echo -e "    ${YELLOW}${url}${NC}"
                        fi
                    done

                    if [ "$TAB_COUNT" -gt 10 ]; then
                        echo -e "  ${YELLOW}... and $((TAB_COUNT - 10)) more tabs${NC}"
                    fi
                else
                    echo -e "  ${YELLOW}No open tabs${NC}"
                fi
            else
                # No jq, display raw JSON summary
                TAB_COUNT=$(echo "$TABS_INFO" | grep -o '"type"' | wc -l)
                echo -e "  ${CYAN}Total ${TAB_COUNT} pages/tabs${NC}"
                echo -e "  ${YELLOW}Note: Install 'jq' to view detailed tab information${NC}"
            fi
        else
            echo -e "  ${YELLOW}Unable to retrieve tab information (Chrome debug port may not be ready)${NC}"
        fi
    fi

else
    echo -e "${RED}${BOLD}📊 Service Status: Not Running${NC}"
    echo ""
    echo -e "${YELLOW}To start the service, run:${NC}"
    echo -e "   ${CYAN}./start-remote-chrome.sh${NC}"
fi

echo ""

# Display help hints
echo -e "${BOLD}Command Help:${NC}"
echo -e "   ${CYAN}./start-remote-chrome.sh${NC}    Start service"
echo -e "   ${CYAN}./stop-remote-chrome.sh${NC}     Stop service"
echo -e "   ${CYAN}./status-remote-chrome.sh${NC}   View status"
echo ""
