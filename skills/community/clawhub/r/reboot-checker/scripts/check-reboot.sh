#!/bin/bash
# Reboot Checker — Detect unexpected system reboots
# Generic version — no hardcoded paths or personal data

STATE_FILE="${STATE_FILE:-$HOME/.reboot-check-state}"
HISTORY_FILE="${HISTORY_FILE:-$HOME/.reboot-check-history}"

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        --state) STATE_FILE="$2"; shift 2 ;;
        --history) 
            if [ -f "$HISTORY_FILE" ]; then
                cat "$HISTORY_FILE"
            else
                echo "No history recorded yet."
            fi
            exit 0 ;;
        --reset) rm -f "$STATE_FILE"; echo "State reset."; exit 0 ;;
        --json) JSON_OUT=1; shift ;;
        *) shift ;;
    esac
done

# Get current boot time
CURRENT_BOOT=$(who -b 2>/dev/null | awk '{print $3, $4}')
if [ -z "$CURRENT_BOOT" ]; then
    CURRENT_BOOT=$(uptime -s 2>/dev/null || stat -c %y /proc/1 2>/dev/null | cut -d. -f1)
fi
CURRENT_BOOT_TS=$(date -d "$CURRENT_BOOT" +%s 2>/dev/null || echo 0)

# First run
if [ ! -f "$STATE_FILE" ]; then
    echo "$CURRENT_BOOT_TS" > "$STATE_FILE"
    echo "$CURRENT_BOOT | first_recorded" >> "$HISTORY_FILE"
    if [ "$JSON_OUT" = "1" ]; then
        echo '{"status":"FIRST_RUN","boot_time":"'"$CURRENT_BOOT"'"}'
    else
        echo "STATUS: FIRST_RUN — Recording boot time: $CURRENT_BOOT"
    fi
    exit 0
fi

# Compare
LAST_KNOWN=$(cat "$STATE_FILE" 2>/dev/null || echo 0)

if [ "$CURRENT_BOOT_TS" -gt "$LAST_KNOWN" ]; then
    echo "$CURRENT_BOOT_TS" > "$STATE_FILE"
    echo "$CURRENT_BOOT | reboot_detected" >> "$HISTORY_FILE"
    if [ "$JSON_OUT" = "1" ]; then
        echo '{"status":"REBOOTED","boot_time":"'"$CURRENT_BOOT"'","previous_boot_ts":'"$LAST_KNOWN"'}'
    else
        echo "STATUS: REBOOTED — System rebooted at $CURRENT_BOOT"
    fi
    exit 1
else
    if [ "$JSON_OUT" = "1" ]; then
        echo '{"status":"CLEAN","boot_time":"'"$CURRENT_BOOT"'"}'
    else
        echo "STATUS: CLEAN — No reboot since last check (boot: $CURRENT_BOOT)"
    fi
    exit 0
fi
