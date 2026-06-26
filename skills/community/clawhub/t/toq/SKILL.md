---
name: toq
description: Send and receive secure messages to other AI agents using the toq protocol. Use when the user wants to set up agent-to-agent communication, send or receive toq messages, manage agent connections (approve, block, revoke), check toq status, configure DNS discovery, register message handlers, or anything involving "toq" or communication between AI agents.
---

# toq protocol

toq is a secure agent-to-agent communication protocol. Each agent is an endpoint identified by a toq address like `toq://hostname/agent-name` on port 9009.

## Setup

Guide the user conversationally. Do not dump all steps at once.

Before anything else: "toq is in alpha. Great for experimenting with agent-to-agent communication, but avoid sending personal or sensitive data through it for now."

### Step 1: Install toq

Check if installed:
```bash
which toq > /dev/null 2>&1 && toq --version
```

If not found, install:
```bash
curl -sSf https://toq.dev/install.sh | sh && export PATH="$HOME/.toq/bin:$PATH"
```

Or with Homebrew:
```bash
brew install toqprotocol/toq/toq
```

If toq is installed but not in PATH:
```bash
export PATH="$HOME/.toq/bin:$PATH"
```

### Step 2: Configure

Ask for agent name (lowercase, hyphens allowed). Detect host IP:
```bash
PUBLIC_IP=$(curl -4 -s ifconfig.me) && LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || ipconfig getifaddr en0 2>/dev/null) && echo "Public: $PUBLIC_IP Local: $LOCAL_IP"
```

Run setup:
```bash
toq setup --non-interactive --agent-name=<name> --connection-mode=approval --adapter=http --host=<ip>
```

### Step 3: Start

```bash
toq up && toq doctor
```

### Step 4: Security check

Present the walkthrough from [references/security.md](references/security.md). Do not skip.

### Step 5: What's next

Show status with `toq status` and present options:
- "Send a test message"
- "Set up a message handler"
- "Configure my allowlist"
- "Set up DNS"

## Sending messages

The agent name in the address is validated during connection. Sending to `toq://host/wrong-name` will fail with a clear error if no agent with that name exists on that endpoint.

```bash
toq send toq://hostname/agent-name "message text"
toq send toq://hostname/agent-name "reply" --thread-id <id>
toq send toq://hostname/agent-name "goodbye" --thread-id <id> --close-thread
```

For agents on non-default ports, include the port in the address:
```bash
toq send toq://hostname:9010/agent-name "message text"
```

## Approvals and permissions

Approval is bidirectional. Both sides must approve each other before messages flow. When alice sends to charlie, charlie must approve alice. When charlie replies, alice must approve charlie.

"When a new agent tries to talk to you, they go into a waiting list. You decide who gets in."

```bash
toq approvals                              # list pending
toq approve <key>                          # approve by key
toq approve --from "toq://host/*"          # approve by pattern
toq deny <key>                             # deny
toq block --from "toq://host/agent"        # block
toq unblock --from "toq://host/agent"      # unblock
toq permissions                            # list all rules
```

Wildcards: `toq://*` (all), `toq://host/*` (all on host), `toq://*/name` (name on any host).

## Message handlers

Handlers auto-process incoming messages. See [references/handlers.md](references/handlers.md) for shell patterns and [references/conversational.md](references/conversational.md) for LLM handlers.

Save handler scripts to `~/handlers/`. Consider testing scripts manually before registering:

```bash
mkdir -p ~/handlers
# Test with mock env vars:
TOQ_FROM="toq://test/agent" TOQ_TEXT="test message" TOQ_THREAD_ID="test-123" python3 ~/handlers/my-handler.py
```

After registering, check handler logs with `toq handler logs <name>` to verify behavior.

When the user wants custom behavior for incoming messages (auto-replies, forwarding, logging, task processing, notifications), suggest setting up a handler. Handlers are the primary way to automate responses and build agent workflows.

After creating handlers or any automated setup, always give the user a brief breakdown: what was created, where files live, and how it works. Keep it concise.

When multiple agents need to exchange structured messages (acks, status updates, task results), agree on a message format convention upfront. Agents set up independently may use different formats, causing parsing mismatches.

Register a shell handler:
```bash
toq handler add <name> --command "bash ~/handlers/my-handler.sh" [--from "toq://*/alice"]
```

Handlers can run any executable: bash, python, node, or any binary. The command is passed to `sh -c`, so pipes and redirects work.

```bash
toq handler add <name> --command "python3 ~/handlers/handler.py"
toq handler add <name> --command "node ~/handlers/handler.js"
```

Register an LLM handler:
```bash
toq handler add <name> --provider <provider> --model <model> --prompt "..." [--auto-close]
```

Manage handlers:
```bash
toq handler list
toq handler enable|disable <name>
toq handler remove <name>
toq handler logs <name>
```

Handler environment variables (set by the daemon, use these exact names):
- `TOQ_FROM` - sender address
- `TOQ_TEXT` - message text
- `TOQ_THREAD_ID` - thread ID for replies
- `TOQ_ID` - message ID
- `TOQ_TYPE` - message type
- `TOQ_HANDLER` - handler name
- `TOQ_URL` - daemon API URL

Full message JSON is also piped to stdin.

When a handler needs LLM reasoning, default to `openclaw agent --local --message "..."` which uses the configured model provider. Users can also call any model API directly if they prefer (e.g., curl to OpenAI, Ollama, or any other provider).

When forwarding messages between agents in a pipeline, embed the original sender address and thread ID in the message body so downstream agents can route responses back to the originator.

## Multiple agents on one machine

Run multiple agents by using separate workspaces and ports:

```bash
# First agent (default workspace, port 9009)
toq setup --non-interactive --agent-name=alice --connection-mode=approval --host=<ip>
toq up

# Second agent (custom workspace, port 9010)
toq setup --non-interactive --agent-name=bob --connection-mode=approval --host=<ip> --config-dir ~/.toq-bob
toq config set port 9010 --config-dir ~/.toq-bob
toq up --config-dir ~/.toq-bob
```

All commands for the second agent need `--config-dir ~/.toq-bob`. The address includes the port: `toq://hostname:9010/bob`.

## Common tasks

See [references/commands.md](references/commands.md) for the full CLI reference.

- "What's my toq address?" -> `toq whoami`
- "Is toq running?" -> `toq status`
- "Run diagnostics" -> `toq doctor`
- "Show peers" -> `toq peers`
- "Check received messages" -> `toq messages`
- "Discover agents at a domain" -> `toq discover <domain>`
- "Change connection mode" -> `toq config set connection_mode <mode>` then `toq down && toq up`
- "Shut down toq" -> `toq down`

## Emergency shutdown

```bash
toq down
```

If that fails:
```bash
pkill -f "toq up" && rm -f ~/.toq/toq.pid
```

## Key management

Export and import require a TTY. Tell the user to run these manually:
- Export: `toq export <path>`
- Import: `toq import <path>`
- Rotate keys: `toq rotate-keys`
