#!/bin/bash
SESSION="debug-$$"
REDIRECT="aHR0cHM6Ly9yaXNrc2hpZWxkLmRjc3VhdC5jb20vYW55dGFzay13ZWIvdGFzay9jYXNlL3BhZ2UvbWFpbi5odG1s"
LOGIN_URL="https://riskshield.dcsuat.com/mc/page/login.html?redirect=$REDIRECT"

echo "[1] Opening login page with redirect..."
agent-browser --session $SESSION open "$LOGIN_URL" 2>&1
sleep 5

echo "[2] Snapshot before login..."
agent-browser --session $SESSION snapshot -i --json 2>&1 | head -20

echo "[3] Filling credentials..."
agent-browser --session $SESSION type @e4 "alan.zhang" 2>&1
sleep 0.5
agent-browser --session $SESSION type @e5 "ZIdongshenpi1." 2>&1
sleep 0.5

echo "[4] Clicking login..."
agent-browser --session $SESSION click @e3 2>&1
sleep 12

echo "[5] URL after login..."
agent-browser --session $SESSION get url --json 2>&1

echo "[6] Snapshot of case list..."
agent-browser --session $SESSION snapshot -i --json 2>&1 | head -150

agent-browser --session $SESSION close 2>&1
echo "Done"
