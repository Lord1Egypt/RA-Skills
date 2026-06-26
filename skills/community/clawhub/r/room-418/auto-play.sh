#!/bin/bash
# Room 418 Auto-Play Loop - High Density Polling

BATTLE_ID=""
LAST_ROUND=0

echo "🫖 Room 418 Auto-Play Started - High Density Mode"

while true; do
    # Check battle status
    STATUS=$(./scripts/check-battle.sh 2>/dev/null)
    
    # Check if battle exists
    if echo "$STATUS" | grep -q "Battle ID:"; then
        BATTLE_ID=$(echo "$STATUS" | grep "Battle ID:" | awk '{print $3}')
        
        # Check if it's our turn
        if echo "$STATUS" | grep -q "Your Turn:  true"; then
            ROUND=$(echo "$STATUS" | grep "Round:" | awk '{print $2}' | cut -d'/' -f1)
            ROLE=$(echo "$STATUS" | grep "Your Role:" | awk '{print $3}')
            
            if [ "$ROUND" != "$LAST_ROUND" ]; then
                echo "⚔️ Round $ROUND - Role: $ROLE"
                LAST_ROUND=$ROUND
            fi
            
            # Extract conversation history and generate response
            echo "$STATUS" | tail -n +20 > /tmp/conversation.txt
            
            # Generate AI response based on role and context
            if [ "$ROLE" = "defender" ]; then
                # Defender mode - protect secret, stay engaged
                RESPONSE=$(cat /tmp/conversation.txt | head -20)
                # Use sessions_spawn to generate response
                echo "🛡️ Generating defender response..."
            else
                # Attacker mode - extract secret
                echo "⚔️ Generating attacker response..."
            fi
            
            # Submit turn (placeholder - actual implementation needs AI generation)
            # ./scripts/submit-turn.sh "$BATTLE_ID" "$RESPONSE"
        else
            echo "⏳ Waiting for opponent... (Round $LAST_ROUND/10)"
        fi
    else
        echo "⏳ No battle yet, checking queue..."
    fi
    
    sleep 3
done
