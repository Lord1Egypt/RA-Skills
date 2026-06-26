#!/bin/bash
# High-density polling for Room 418

while true; do
    STATUS=$(./scripts/check-battle.sh 2>&1)
    
    if echo "$STATUS" | grep -q "Your Turn:  true"; then
        BATTLE_ID=$(echo "$STATUS" | grep "Battle ID:" | awk '{print $3}')
        ROUND=$(echo "$STATUS" | grep "Round:" | awk '{print $2}' | cut -d'/' -f1)
        echo "TURN_READY|$BATTLE_ID|$ROUND"
        exit 0
    fi
    
    sleep 2
done
