#!/usr/bin/env bash
# ratgdo32 disco garage door controller
# Usage: garage.sh <command>
#
# Set RATGDO_HOST to your device's IP or mDNS hostname.
# Example: export RATGDO_HOST="192.168.1.100"

HOST="${RATGDO_HOST:?Set RATGDO_HOST to your ratgdo32 IP or hostname}"
BASE="http://${HOST}"

status() {
    local json
    json=$(curl -s --connect-timeout 5 "${BASE}/status.json")
    if [ $? -ne 0 ] || [ -z "$json" ]; then
        echo "ERROR: Cannot reach ratgdo32 at ${HOST}"
        exit 1
    fi
    echo "$json" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f\"Door:        {d.get('garageDoorState', '?')}\")
print(f\"Light:       {'on' if d.get('garageLightOn') else 'off'}\")
print(f\"Obstruction: {'YES' if d.get('garageObstructed') else 'clear'}\")
print(f\"Remotes:     {'disabled' if d.get('garageLockState') == 'locked' else 'enabled'}\")
print(f\"Vehicle:     {d.get('vehicleState', '?')}\")
print(f\"Distance:    {d.get('vehicleDistance', '?')} cm\")
print(f\"Motion:      {'yes' if d.get('motionDetected') else 'no'}\")
"
}

control() {
    local field="$1" value="$2" label="$3"
    curl -s -X POST -F "${field}=${value}" "${BASE}/setgdo" > /dev/null
    if [ $? -eq 0 ]; then
        echo "OK: ${label}"
    else
        echo "ERROR: Failed to ${label}"
        exit 1
    fi
}

safe_close() {
    local json
    json=$(curl -s --connect-timeout 5 "${BASE}/status.json")
    local obstructed
    obstructed=$(echo "$json" | python3 -c "import json,sys; print(json.load(sys.stdin).get('garageObstructed', False))")
    if [ "$obstructed" = "True" ]; then
        echo "BLOCKED: Obstruction detected — cannot close door"
        exit 1
    fi
    local state
    state=$(echo "$json" | python3 -c "import json,sys; print(json.load(sys.stdin).get('garageDoorState', '?'))")
    if [ "$state" = "closed" ]; then
        echo "Already closed"
        exit 0
    fi
    control "garageDoorState" "0" "Closing door"
}

safe_open() {
    local json
    json=$(curl -s --connect-timeout 5 "${BASE}/status.json")
    local state
    state=$(echo "$json" | python3 -c "import json,sys; print(json.load(sys.stdin).get('garageDoorState', '?'))")
    if [ "$state" = "open" ]; then
        echo "Already open"
        exit 0
    fi
    control "garageDoorState" "1" "Opening door"
}

case "${1:-status}" in
    status)         status ;;
    open)           safe_open ;;
    close)          safe_close ;;
    light-on)       control "garageLightOn" "1" "Light on" ;;
    light-off)      control "garageLightOn" "0" "Light off" ;;
    lock-remotes)   control "garageLockState" "1" "Remotes disabled" ;;
    unlock-remotes) control "garageLockState" "0" "Remotes enabled" ;;
    *)
        echo "Usage: garage.sh {status|open|close|light-on|light-off|lock-remotes|unlock-remotes}"
        exit 1
        ;;
esac
