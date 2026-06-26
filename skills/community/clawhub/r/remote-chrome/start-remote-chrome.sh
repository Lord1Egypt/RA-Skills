#!/bin/bash
# Start Chrome Remote Access Service
# Provides browser access via noVNC

# Configuration parameters (defaults, can be overridden via command line)
DISPLAY_NUM=99
VNC_PORT=5900
NOVNC_PORT=6080
CHROME_DEBUG_PORT=9222
SCREEN_SIZE="1600x1200x24"  # Format: WxH x color depth
CHROME_BIN="chromium"  # Can be changed to google-chrome-stable
VNC_PASSWORD=$(openssl rand -hex 6)  # Auto-generate 12-character random password

# Log control
VERBOSE=false
FOREGROUND=false  # Default to background mode

# Proxy settings (configurable via command line)
HTTP_PROXY=""
HTTPS_PROXY=""
NO_PROXY=""

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -f|--foreground)
            FOREGROUND=true
            shift
            ;;
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
        --screen-size)
            if [ -n "$2" ] && [[ "$2" != -* ]]; then
                SCREEN_SIZE="$2"
                shift 2
            else
                echo -e "${RED}✗ Error: --screen-size requires a resolution (e.g., 1920x1080x24)${NC}"
                exit 1
            fi
            ;;
        --proxy)
            if [ -n "$2" ] && [[ "$2" != -* ]]; then
                HTTP_PROXY="$2"
                HTTPS_PROXY="$2"
                shift 2
            else
                echo -e "${RED}✗ Error: --proxy requires a URL argument${NC}"
                exit 1
            fi
            ;;
        --proxy-bypass)
            if [ -n "$2" ] && [[ "$2" != -* ]]; then
                NO_PROXY="$2"
                shift 2
            else
                echo -e "${RED}✗ Error: --proxy-bypass requires a list argument${NC}"
                exit 1
            fi
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -v, --verbose                Enable verbose logging"
            echo "  -f, --foreground             Run in foreground mode (default: background)"
            echo "  --vnc-port <port>            VNC server port (default: 5900)"
            echo "  --novnc-port <port>          noVNC web access port (default: 6080)"
            echo "  --chrome-debug-port <port>   Chrome remote debugging port (default: 9222)"
            echo "  --screen-size <WxHxD>        Screen resolution (default: 1600x1200x24)"
            echo "  --proxy <url>                Set HTTP/HTTPS proxy server"
            echo "  --proxy-bypass <list>        Set proxy bypass list (comma-separated)"
            echo "  -h, --help                   Display help information"
            echo ""
            echo "Examples:"
            echo "  $0 --vnc-port 5901 --novnc-port 6081"
            echo "  $0 --screen-size 1920x1080x24"
            echo "  $0 --proxy http://proxy.example.com:8080"
            echo "  $0 --proxy http://proxy.example.com:8080 --proxy-bypass 'localhost,*.example.com'"
            echo "  $0 -v -f"
            exit 0
            ;;
        *)
            echo -e "${RED}✗ Error: Unknown parameter $1${NC}"
            echo "Use -h or --help to view help"
            exit 1
            ;;
    esac
done

# Use environment variables if not set via command line
if [ -z "$HTTP_PROXY" ] && [ -n "$http_proxy" ]; then
    HTTP_PROXY="$http_proxy"
fi
if [ -z "$HTTPS_PROXY" ] && [ -n "$https_proxy" ]; then
    HTTPS_PROXY="$https_proxy"
fi
if [ -z "$NO_PROXY" ] && [ -n "$no_proxy" ]; then
    NO_PROXY="$no_proxy"
fi

echo -e "${GREEN}${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║   Starting Chrome Remote Access Service    ║${NC}"
echo -e "${GREEN}${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""

# Log functions
log_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "$@"
    fi
}

log_info() {
    echo -e "$@"
}

log_error() {
    echo -e "$@"
}

# Helper function: check if command exists
check_command() {
    local cmd=$1
    local package=$2
    if ! command -v $cmd >/dev/null 2>&1; then
        return 1
    fi
    return 0
}

# Check required dependencies
check_dependencies() {
    local missing_deps=()
    local install_cmds=()

    # Check Xvfb
    if ! check_command Xvfb "xvfb"; then
        missing_deps+=("Xvfb (Virtual X Server)")
        install_cmds+=("sudo apt-get install xvfb")
    fi

    # Check x11vnc
    if ! check_command x11vnc "x11vnc"; then
        missing_deps+=("x11vnc (VNC Server)")
        install_cmds+=("sudo apt-get install x11vnc")
    fi

    # Check openssl (for password generation)
    if ! check_command openssl "openssl"; then
        missing_deps+=("openssl (Password Generator)")
        install_cmds+=("sudo apt-get install openssl")
    fi

    # Check noVNC (multiple ways)
    local novnc_found=false
    for path in /usr/share/novnc/utils/launch.sh /usr/share/novnc/utils/novnc_proxy /usr/share/novnc/utils/novnc_proxy.py; do
        if [ -f "$path" ]; then
            novnc_found=true
            break
        fi
    done

    if [ "$novnc_found" = false ]; then
        # Try to find via which
        if ! check_command websockify "websockify" && ! check_command novnc_proxy "novnc"; then
            missing_deps+=("noVNC (Web VNC Client)")
            install_cmds+=("sudo apt-get install novnc websockify")
        fi
    fi

    # Check Chrome/Chromium
    local chrome_found=false
    for bin in chromium chromium-browser google-chrome-stable google-chrome; do
        if check_command $bin ""; then
            chrome_found=true
            CHROME_BIN=$bin
            break
        fi
    done

    if [ "$chrome_found" = false ]; then
        missing_deps+=("Chromium or Google Chrome")
        install_cmds+=("sudo apt-get install chromium or download Chrome from official website")
    fi

    # If there are missing dependencies, show error message and exit
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo ""
        log_error "${RED}${BOLD}✗ Error: Missing required dependencies${NC}"
        echo ""
        echo -e "${YELLOW}The following dependencies are not installed:${NC}"
        for i in "${!missing_deps[@]}"; do
            echo -e "  ${RED}✗${NC} ${missing_deps[$i]}"
        done
        echo ""
        echo -e "${YELLOW}Installation commands:${NC}"
        for cmd in "${install_cmds[@]}"; do
            echo -e "  ${CYAN}${cmd}${NC}"
        done
        echo ""
        echo -e "${YELLOW}Note: After installing dependencies, re-run this script to start the service${NC}"
        echo ""
        exit 1
    fi

    log_verbose "${GREEN}✓ All dependencies installed${NC}"
}

# Check dependencies
log_info "${YELLOW}• Checking dependencies...${NC}"
check_dependencies

# Helper function: check if port is in use
check_port() {
    local port=$1
    local name=$2
    if ss -tuln 2>/dev/null | grep -q ":${port} " || netstat -tuln 2>/dev/null | grep -q ":${port} "; then
        log_error "${RED}✗ Error: Port ${port} ($name) is already in use${NC}"
        echo "Please run ./stop-remote-chrome.sh first, or modify the port number in the script"
        exit 1
    fi
}

# Check port usage
log_info "${YELLOW}• Checking port availability...${NC}"
check_port $VNC_PORT "VNC"
check_port $NOVNC_PORT "noVNC"
check_port $CHROME_DEBUG_PORT "Chrome Debug"

# Cleanup function
cleanup() {
    echo ""
    log_info "${YELLOW}Stopping services...${NC}"
    pkill -f "x11vnc.*:${DISPLAY_NUM}" 2>/dev/null || true
    pkill -f "websockify.*${NOVNC_PORT}" 2>/dev/null || true
    pkill -f "novnc_proxy.*${NOVNC_PORT}" 2>/dev/null || true
    pkill -f "Xvfb :${DISPLAY_NUM}" 2>/dev/null || true
    pkill -f "${CHROME_BIN}.*--display=:${DISPLAY_NUM}" 2>/dev/null || true
    log_info "${GREEN}✓ Services stopped${NC}"
}

# Catch exit signal, cleanup processes
trap cleanup EXIT

# Cleanup old processes
log_info "${YELLOW}• Cleaning up old processes...${NC}"
cleanup
sleep 1

# 1. Start virtual display Xvfb
log_info "${YELLOW}• Starting virtual display Xvfb :${DISPLAY_NUM} (${SCREEN_SIZE%x*})...${NC}"
Xvfb :${DISPLAY_NUM} -screen 0 ${SCREEN_SIZE} >/dev/null 2>&1 &
XVFB_PID=$!
sleep 2

# Verify Xvfb started
if ! kill -0 $XVFB_PID 2>/dev/null; then
    log_error "${RED}✗ Error: Xvfb failed to start${NC}"
    exit 1
fi
log_info "${GREEN}  ✓ Xvfb started successfully${NC}"
log_verbose "    PID: ${XVFB_PID}"

# 2. Start x11vnc server
log_info "${YELLOW}• Starting x11vnc (port ${VNC_PORT})...${NC}"
# Save password to file for status script to read
echo "${VNC_PASSWORD}" > /tmp/remote-chrome-vnc-password.txt
chmod 600 /tmp/remote-chrome-vnc-password.txt
x11vnc -display :${DISPLAY_NUM} -forever -shared -rfbport ${VNC_PORT} -passwd ${VNC_PASSWORD} -bg -o /tmp/x11vnc.log >/dev/null 2>&1
sleep 2
log_info "${GREEN}  ✓ x11vnc started successfully${NC}"

# 3. Start noVNC Web service
log_info "${YELLOW}• Starting noVNC (port ${NOVNC_PORT})...${NC}"
NOVNC_LAUNCHER=""
for path in /usr/share/novnc/utils/launch.sh /usr/share/novnc/utils/novnc_proxy /usr/share/novnc/utils/novnc_proxy.py; do
    if [ -f "$path" ]; then
        NOVNC_LAUNCHER="$path"
        break
    fi
done

if [ -z "$NOVNC_LAUNCHER" ]; then
    # Try to find via which
    NOVNC_LAUNCHER=$(which websockify novnc_proxy 2>/dev/null | head -1)
fi

if [ -z "$NOVNC_LAUNCHER" ]; then
    log_error "${RED}✗ Error: noVNC launch script not found${NC}"
    echo "Tried paths:"
    echo "  - /usr/share/novnc/utils/launch.sh"
    echo "  - /usr/share/novnc/utils/novnc_proxy"
    echo "  - websockify (via PATH)"
    exit 1
fi

# Determine launch method
if [[ "$NOVNC_LAUNCHER" == *"launch.sh"* ]]; then
    $NOVNC_LAUNCHER --vnc localhost:${VNC_PORT} --listen ${NOVNC_PORT} >/dev/null 2>&1 &
elif [[ "$NOVNC_LAUNCHER" == *"novnc_proxy"* ]]; then
    $NOVNC_LAUNCHER --vnc localhost:${VNC_PORT} --listen ${NOVNC_PORT} >/dev/null 2>&1 &
else
    # Use websockify
    $NOVNC_LAUNCHER --web /usr/share/novnc localhost:${NOVNC_PORT} localhost:${VNC_PORT} >/dev/null 2>&1 &
fi
NOVNC_PID=$!
sleep 2
log_info "${GREEN}  ✓ noVNC started successfully${NC}"
log_verbose "    PID: ${NOVNC_PID}"

# 4. Start Chrome/Chromium
PROXY_MSG=""
CHROME_PROXY_ARGS=""

if [ -n "$HTTP_PROXY" ]; then
    PROXY_MSG=" (using proxy: ${HTTP_PROXY})"
    CHROME_PROXY_ARGS="--proxy-server=${HTTP_PROXY}"

    if [ -n "$NO_PROXY" ]; then
        CHROME_PROXY_ARGS="${CHROME_PROXY_ARGS} --proxy-bypass-list=${NO_PROXY}"
    fi
fi

log_info "${YELLOW}• Starting ${CHROME_BIN}${PROXY_MSG}...${NC}"

# Extract width and height from SCREEN_SIZE (format: WxHxD)
SCREEN_WIDTH=$(echo $SCREEN_SIZE | cut -d'x' -f1)
SCREEN_HEIGHT=$(echo $SCREEN_SIZE | cut -d'x' -f2)

if [ "$VERBOSE" = true ]; then
    DISPLAY=:${DISPLAY_NUM} ${CHROME_BIN} \
        --remote-debugging-port=${CHROME_DEBUG_PORT} \
        --disable-gpu \
        --disable-dev-shm-usage \
        $CHROME_PROXY_ARGS \
        --window-size=${SCREEN_WIDTH},${SCREEN_HEIGHT} \
        --start-maximized \
        --disable-infobars \
        --disable-extensions \
        about:blank &
else
    DISPLAY=:${DISPLAY_NUM} ${CHROME_BIN} \
        --remote-debugging-port=${CHROME_DEBUG_PORT} \
        --disable-gpu \
        --disable-dev-shm-usage \
        $CHROME_PROXY_ARGS \
        --window-size=${SCREEN_WIDTH},${SCREEN_HEIGHT} \
        --start-maximized \
        --disable-infobars \
        --disable-extensions \
        about:blank >/dev/null 2>&1 &
fi
CHROME_PID=$!
sleep 3

# Verify Chrome started
if ! kill -0 $CHROME_PID 2>/dev/null; then
    log_error "${RED}✗ Warning: ${CHROME_BIN} process exited, may have failed to start${NC}"
    echo "Service will continue running, but browser may not be available"
else
    log_info "${GREEN}  ✓ ${CHROME_BIN} started successfully${NC}"
    log_verbose "    PID: ${CHROME_PID}"
fi

# Get host IP
HOST_IP=$(hostname -I | awk '{print $1}')
HOSTNAME=$(hostname | cut -d'.' -f1)

# Beautified output
echo ""
echo -e "${GREEN}${BOLD}═════════════════════════════════════════════${NC}"
echo -e "${GREEN}${BOLD}          ✓ Service Started Successfully!${NC}"
echo -e "${GREEN}${BOLD}═════════════════════════════════════════════${NC}"
echo ""
log_info "${BOLD}📱 Remote Access URL (Recommended):${NC}"
echo -e "   ${CYAN}${BOLD}http://${HOST_IP}:${NOVNC_PORT}/vnc.html?host=${HOST_IP}&port=${NOVNC_PORT}&password=${VNC_PASSWORD}&autoconnect=true${NC}"
echo ""
log_info "${BOLD}💻 Or connect via VNC client:${NC}"
echo -e "   ${CYAN}${BOLD}${HOST_IP}:${VNC_PORT}${NC} ${YELLOW}(Password: ${VNC_PASSWORD})${NC}"
echo ""
log_info "${BOLD}🔑 VNC Password: ${CYAN}${BOLD}${VNC_PASSWORD}${NC}"

# Show detailed info in verbose mode
if [ "$VERBOSE" = true ]; then
    echo ""
    log_info "${BOLD}📊 Process Information:${NC}"
    echo -e "   Xvfb:    ${XVFB_PID}"
    echo -e "   x11vnc:  $(pgrep -f "x11vnc.*:${DISPLAY_NUM}")"
    echo -e "   noVNC:   ${NOVNC_PID}"
    if kill -0 $CHROME_PID 2>/dev/null; then
        echo -e "   Chrome:  ${CHROME_PID}"
    fi
    echo ""
    log_info "${BOLD}⚙️  Configuration:${NC}"
    echo -e "   Resolution:    ${SCREEN_SIZE%x*}"
    echo -e "   VNC Port:      ${VNC_PORT}"
    echo -e "   noVNC Port:    ${NOVNC_PORT}"
    echo -e "   Debug Port:    ${CHROME_DEBUG_PORT}"
    if [ -n "$HTTP_PROXY" ]; then
        echo -e "   Proxy:         ${HTTP_PROXY}"
        if [ -n "$NO_PROXY" ]; then
            echo -e "   Bypass:        ${NO_PROXY}"
        fi
    else
        echo -e "   Proxy:         None (direct connection)"
    fi
fi
echo ""
if [ "$FOREGROUND" = true ]; then
    echo -e "${YELLOW}Note: Press Ctrl+C to stop all services${NC}"
    echo ""

    # Keep script running and monitor critical processes
    while true; do
        # Check if critical processes are still running
        if ! kill -0 $XVFB_PID 2>/dev/null; then
            log_error "${RED}✗ Error: Xvfb process exited unexpectedly${NC}"
            exit 1
        fi
        if [ -n "$NOVNC_PID" ] && ! kill -0 $NOVNC_PID 2>/dev/null; then
            log_error "${RED}✗ Error: noVNC process exited unexpectedly${NC}"
            exit 1
        fi
        sleep 5
    done
else
    echo -e "${YELLOW}Note: Service is running in background. Use ./status-remote-chrome.sh to check status${NC}"
    echo -e "${YELLOW}      Use ./stop-remote-chrome.sh to stop the service${NC}"
    echo ""

    # Disable trap, let processes continue in background
    trap - EXIT
    exit 0
fi
