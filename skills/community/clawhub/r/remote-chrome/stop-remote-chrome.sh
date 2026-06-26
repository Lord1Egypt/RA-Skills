#!/bin/bash
# Stop Chrome Remote Access Service

# Configuration parameters (must match start script)
DISPLAY_NUM=99
VNC_PORT=5900
NOVNC_PORT=6080
CHROME_BIN="chromium"  # Can be changed to google-chrome-stable

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${YELLOW}Stopping Chrome Remote Access Service...${NC}"

# Find and display currently running processes
echo ""
echo -e "${BOLD}Currently running processes:${NC}"

XVFB_PID=$(pgrep -f "Xvfb :${DISPLAY_NUM}")
if [ -n "$XVFB_PID" ]; then
    echo "  Xvfb:    $XVFB_PID"
fi

X11VNC_PID=$(pgrep -f "x11vnc.*:${DISPLAY_NUM}")
if [ -n "$X11VNC_PID" ]; then
    echo "  x11vnc:  $X11VNC_PID"
fi

WEBSOCKIFY_PID=$(pgrep -f "websockify.*${NOVNC_PORT}")
if [ -n "$WEBSOCKIFY_PID" ]; then
    echo "  websockify: $WEBSOCKIFY_PID"
fi

CHROME_PID=$(pgrep -f "${CHROME_BIN}.*--display=:${DISPLAY_NUM}")
if [ -n "$CHROME_PID" ]; then
    echo "  Chrome:  $CHROME_PID"
fi

# Stop processes
echo ""
echo -e "${YELLOW}Stopping services...${NC}"

if [ -n "$X11VNC_PID" ]; then
    kill $X11VNC_PID 2>/dev/null && echo -e "${GREEN}✓ x11vnc stopped${NC}"
fi

if [ -n "$WEBSOCKIFY_PID" ]; then
    kill $WEBSOCKIFY_PID 2>/dev/null && echo -e "${GREEN}✓ websockify stopped${NC}"
fi

if [ -n "$CHROME_PID" ]; then
    kill $CHROME_PID 2>/dev/null && echo -e "${GREEN}✓ Chrome stopped${NC}"
    # Wait for Chrome to exit gracefully
    sleep 2
    # If still running, force kill all related processes
    pkill -9 -f "${CHROME_BIN}.*--display=:${DISPLAY_NUM}" 2>/dev/null
fi

if [ -n "$XVFB_PID" ]; then
    kill $XVFB_PID 2>/dev/null && echo -e "${GREEN}✓ Xvfb stopped${NC}"
fi

# Clean up any remaining processes
sleep 1
pkill -f "x11vnc.*:${DISPLAY_NUM}" 2>/dev/null
pkill -f "websockify.*${NOVNC_PORT}" 2>/dev/null
pkill -f "novnc_proxy.*${NOVNC_PORT}" 2>/dev/null
pkill -f "Xvfb :${DISPLAY_NUM}" 2>/dev/null
pkill -f "${CHROME_BIN}.*--display=:${DISPLAY_NUM}" 2>/dev/null

# Clean up password file
rm -f /tmp/remote-chrome-vnc-password.txt 2>/dev/null

echo ""
echo -e "${GREEN}${BOLD}✓ Service stopped${NC}"

# Check if ports are released
echo ""
echo -e "${YELLOW}Checking port status:${NC}"
if ss -tuln 2>/dev/null | grep -q ":${VNC_PORT} " || netstat -tuln 2>/dev/null | grep -q ":${VNC_PORT} "; then
    echo -e "${RED}✗ Port ${VNC_PORT} is still in use${NC}"
else
    echo -e "${GREEN}✓ Port ${VNC_PORT} released${NC}"
fi

if ss -tuln 2>/dev/null | grep -q ":${NOVNC_PORT} " || netstat -tuln 2>/dev/null | grep -q ":${NOVNC_PORT} "; then
    echo -e "${RED}✗ Port ${NOVNC_PORT} is still in use${NC}"
else
    echo -e "${GREEN}✓ Port ${NOVNC_PORT} released${NC}"
fi
