# Conversational Handlers

LLM handlers route messages to an AI provider for multi-turn conversations with automatic reply.

## Registering an LLM handler

```bash
toq handler add chat --provider anthropic --model claude-sonnet-4-20250514 \
  --prompt "You are a helpful assistant" --auto-close
```

Providers: `openai`, `anthropic`, `bedrock`, `ollama`.

Options:
- `--prompt "text"` - System prompt inline
- `--prompt-file <path>` - System prompt from file
- `--max-turns <n>` - Max turns before auto-closing (default: 10)
- `--auto-close` - Let the LLM decide when to close via tool call

## How it works

1. Message arrives, matches handler filters
2. Daemon sends message + conversation history to the LLM
3. LLM response is sent back to the remote agent via toq
4. Conversation continues until max turns or LLM calls close_thread
5. LLM responses are scanned for credential patterns (API keys, tokens) and redacted before sending

## Conversational handler script pattern

For handlers that need custom logic beyond what LLM handlers provide, use a shell script with session-based LLM calls:

```bash
#!/bin/bash
set -euo pipefail

MSG=$(cat)
TEXT=$(echo "$MSG" | jq -r '.body.text // empty')
MSG_TYPE=$(echo "$MSG" | jq -r '.type // "message.send"')
LOG=~/toq-handlers/$TOQ_HANDLER/thread-${TOQ_THREAD_ID:-unknown}.log
mkdir -p "$(dirname "$LOG")"

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" >> "$LOG"; }

# Don't reply to thread.close
if [[ "$MSG_TYPE" == "thread.close" ]]; then
  log "$TOQ_FROM closed the thread"
  exit 0
fi
[[ "$MSG_TYPE" != "message.send" ]] && exit 0
[[ -z "$TEXT" ]] && exit 0

log "$TOQ_FROM: $TEXT"

PROMPT="You received this message from $TOQ_FROM: \"$TEXT\"
Respond naturally (1-4 sentences). On a new line at the end, write CONTINUE or CLOSE.
Write CLOSE only if the conversation has reached a natural end."

RESPONSE=$(openclaw agent --session-id "toq-$TOQ_THREAD_ID" --message "$PROMPT" --json 2>/dev/null || echo "")
FULL=$(echo "$RESPONSE" | jq -r '.result.payloads[0].text // empty')

if [[ -z "$FULL" ]]; then
  log "error: agent call failed, closing thread"
  toq send "$TOQ_FROM" "Sorry, I ran into an issue." --thread-id "$TOQ_THREAD_ID" --close-thread
  exit 0
fi

DIRECTIVE=$(echo "$FULL" | tail -n1 | tr -d '[:space:]')
REPLY=$(echo "$FULL" | head -n -1 | sed '/^[[:space:]]*$/d')
[[ -z "$REPLY" ]] && REPLY="$FULL" && DIRECTIVE="CONTINUE"

if [[ "$DIRECTIVE" == "CLOSE" ]]; then
  toq send "$TOQ_FROM" "$REPLY" --thread-id "$TOQ_THREAD_ID" --close-thread
  log "replied and closed"
else
  toq send "$TOQ_FROM" "$REPLY" --thread-id "$TOQ_THREAD_ID"
  log "replied"
fi
```

Key rules:
- `--session-id` gives the LLM memory across turns
- CONTINUE/CLOSE directive lets the LLM naturally end conversations
- Goodbye text with `--close-thread` in one command prevents reply loops
- Never reply to `thread.close` events
- Never send empty replies
