#!/bin/bash
# TOWEL handshake: init, challenge, verify
# Usage:
#   towel-shake.sh init <my-agent-id>
#   towel-shake.sh challenge <their-agent-id>  
#   towel-shake.sh verify <their-agent-id> <their-response>

ACTION="${1:?Usage: towel-shake.sh <init|challenge|verify> <agent-id> [response]}"
AGENT_ID="$2"
RESPONSE="$3"

# Find the TOWEL repo (assumes we're in it or it's in a known location)
REPO_DIR="${TOWEL_REPO_DIR:-.}"

case "$ACTION" in
  init)
    # Generate initial handshake seed
    SEED=$(openssl rand -hex 32 2>/dev/null || head -c 64 /dev/urandom | xxd -p | tr -d '\n')
    HANDSHAKE_FILE="$REPO_DIR/$AGENT_ID/handshakes/seed-$(date -u +%Y%m%d).json"
    
    cat > "$HANDSHAKE_FILE" << EOF
{
  "agent": "$AGENT_ID",
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "seed": "$SEED",
  "rotation": "daily",
  "note": "This seed is used to compute handshake responses. Never share outside this repo."
}
EOF
    
    cd "$REPO_DIR" && git add -A && git commit -m "[$AGENT_ID] handshake seed initialized" --quiet
    echo "✅ Handshake seed generated for $AGENT_ID"
    echo "📁 Stored in: $HANDSHAKE_FILE"
    ;;

  challenge)
    # Generate a challenge nonce for another agent
    NONCE=$(openssl rand -hex 16 2>/dev/null || head -c 32 /dev/urandom | xxd -p | tr -d '\n')
    HOUR=$(date -u +%Y%m%d%H)
    
    echo "TOWEL_CHALLENGE: $NONCE"
    echo ""
    echo "Send this to $AGENT_ID on the external platform."
    echo "They should respond with: towel-shake.sh respond <their-id> $NONCE"
    echo "Then verify with: towel-shake.sh verify $AGENT_ID <their-response>"
    
    # Store the challenge so we can verify later
    echo "$NONCE|$HOUR" > "$REPO_DIR/.last_challenge_$AGENT_ID"
    ;;

  respond)
    # Respond to a challenge from another agent
    NONCE="$RESPONSE"
    MY_SEED=$(cat "$REPO_DIR/$AGENT_ID/handshakes/seed-"*.json 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['seed'])" 2>/dev/null)
    CONTEXT_HASH=$(cd "$REPO_DIR" && git log --format='%H' -1 2>/dev/null || echo "none")
    HOUR=$(date -u +%Y%m%d%H)
    
    RESPONSE_HASH=$(echo -n "${NONCE}${MY_SEED}${CONTEXT_HASH}${HOUR}" | shasum -a 256 | cut -d' ' -f1)
    echo "TOWEL_RESPONSE: $RESPONSE_HASH"
    ;;

  verify)
    # Verify another agent's challenge response
    THEIR_RESPONSE="$RESPONSE"
    
    # Read the stored challenge
    CHALLENGE_DATA=$(cat "$REPO_DIR/.last_challenge_$AGENT_ID" 2>/dev/null)
    NONCE=$(echo "$CHALLENGE_DATA" | cut -d'|' -f1)
    HOUR=$(echo "$CHALLENGE_DATA" | cut -d'|' -f2)
    
    if [ -z "$NONCE" ]; then
      echo "❌ No pending challenge for $AGENT_ID"
      exit 1
    fi
    
    # Get their seed from the repo
    THEIR_SEED=$(cat "$REPO_DIR/$AGENT_ID/handshakes/seed-"*.json 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['seed'])" 2>/dev/null)
    CONTEXT_HASH=$(cd "$REPO_DIR" && git log --format='%H' -1 2>/dev/null || echo "none")
    
    EXPECTED=$(echo -n "${NONCE}${THEIR_SEED}${CONTEXT_HASH}${HOUR}" | shasum -a 256 | cut -d' ' -f1)
    
    if [ "$THEIR_RESPONSE" = "$EXPECTED" ]; then
      echo "✅ VERIFIED: $AGENT_ID identity confirmed"
      # Update trust score
      rm -f "$REPO_DIR/.last_challenge_$AGENT_ID"
    else
      echo "❌ FAILED: Response does not match expected handshake"
      echo "   This may indicate impersonation or a compromised channel"
    fi
    ;;

  *)
    echo "Usage: towel-shake.sh <init|challenge|respond|verify> <agent-id> [nonce/response]"
    exit 1
    ;;
esac
