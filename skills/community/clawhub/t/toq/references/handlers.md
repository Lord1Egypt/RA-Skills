# Shell Handlers

Handlers are scripts the toq daemon runs automatically when messages arrive. The daemon manages spawning, filtering, logging, and stopping. Handlers can be any executable: bash, python, node, or any binary.

## Environment variables

Every handler receives: `TOQ_FROM`, `TOQ_TEXT`, `TOQ_THREAD_ID`, `TOQ_TYPE`, `TOQ_ID`, `TOQ_HANDLER`, `TOQ_URL`. Full message JSON is piped to stdin.

## Creating a handler

Write the script, then register it:

```bash
mkdir -p ~/handlers

cat > ~/handlers/log-alice.sh << 'EOF'
#!/bin/bash
echo "[$(date)] From: $TOQ_FROM - $TOQ_TEXT" >> ~/alice-messages.log
EOF
chmod +x ~/handlers/log-alice.sh

toq handler add alice-logger --command "bash ~/handlers/log-alice.sh" --from "toq://*/alice"
```

Python handler example:
```bash
cat > ~/handlers/smart-reply.py << 'EOF'
#!/usr/bin/env python3
import os, json, subprocess, sys

msg = json.load(sys.stdin)
text = os.environ.get("TOQ_TEXT", "")
sender = os.environ.get("TOQ_FROM", "")
thread = os.environ.get("TOQ_THREAD_ID", "")

# Process the message and reply
subprocess.run(["toq", "send", sender, f"Got your message: {text}", "--thread-id", thread])
EOF
chmod +x ~/handlers/smart-reply.py

toq handler add smart-reply --command "python3 ~/handlers/smart-reply.py"
```

## Common patterns

### Auto-reply within a thread
```bash
#!/bin/bash
toq send "$TOQ_FROM" "Thanks, I'll get back to you soon." --thread-id "$TOQ_THREAD_ID"
```

### Close a conversation
```bash
#!/bin/bash
toq send "$TOQ_FROM" "Goodbye!" --thread-id "$TOQ_THREAD_ID" --close-thread
```

Important: always send the goodbye text and `--close-thread` as a single command. Two separate messages cause a race where the remote handler replies before seeing the close.

### Forward to a file
```bash
#!/bin/bash
echo "[$(date)] $TOQ_FROM: $TOQ_TEXT" >> ~/toq-inbox.log
```

### Parse JSON from stdin
```bash
#!/bin/bash
MSG=$(cat)
FROM=$(echo "$MSG" | jq -r '.from')
TEXT=$(echo "$MSG" | jq -r '.body.text // empty')
```

### Python handler with state management
```python
#!/usr/bin/env python3
import os, json, sys, subprocess
from pathlib import Path

STATE_FILE = Path.home() / "handler-state.json"

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

msg = json.load(sys.stdin)
text = os.environ["TOQ_TEXT"]
sender = os.environ["TOQ_FROM"]
thread = os.environ.get("TOQ_THREAD_ID", "")

state = load_state()
# ... process message, update state ...
save_state(state)
```

## Filter rules

```bash
# Only from a specific host
toq handler add h --command "bash log.sh" --from "toq://1.2.3.4/*"

# Multiple hosts (OR)
toq handler add h --command "bash log.sh" --from "toq://a.com/*" --from "toq://b.com/*"

# Only message.send type
toq handler add h --command "bash log.sh" --type message.send

# Combined: from host AND specific type (AND)
toq handler add h --command "bash log.sh" --from "toq://host/*" --type message.send
```

## Do not add --type filters to conversational handlers

The handler must receive `thread.close` events so it knows when the remote agent ended the conversation. The script handles type checking internally.

## Common pitfalls

When mixing Python and bash in handlers, watch for type mismatches. Python's `json.load()` returns `True`/`False` (capital), not `true`/`false`. Normalize before shell comparisons:
```python
print(str(data.get("resolved", False)).lower())  # prints "true" or "false"
```
