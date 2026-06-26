# ConvoAI Advanced / Debugging / Ops

For requests where the user already has a working ConvoAI baseline, or is debugging / hardening an existing setup.
Classify the mode in [README.md](README.md) first. If no working baseline exists, use [quickstart.md](quickstart.md).

## Step 1: Confirm Baseline

One sentence: what's working, which platform/repo, what needs to change.

Examples:
- "Web ConvoAI sample running; adding MCP tools."
- "Existing project creates agents; debugging TTS vendor auth."

## Step 2: Route by Type

### Features

| Feature | Local doc | Fetch if needed |
|---------|-----------|-----------------|
| MCP / tools | `convoai-restapi/start-agent.md` (`mcp_servers`) | ConvoAI MCP user guide |
| history | `convoai-restapi/get-history.md` | - |
| interrupt | `convoai-restapi/agent-interrupt.md` | - |
| speak | `convoai-restapi/agent-speak.md` | - |
| update LLM | `convoai-restapi/agent-update.md` | - |
| template variables | `convoai-restapi/start-agent.md` (`template_variables`) | - |
| status query | `convoai-restapi/query-agent-status.md` | - |
| stop agent | `convoai-restapi/stop-agent.md` | - |
| filler words | `convoai-restapi/start-agent.md` (`filler_words`) | - |
| turn detection | `convoai-restapi/start-agent.md` (`turn_detection`) | - |
| SAL (voice lock) | `convoai-restapi/start-agent.md` (`sal`) | - |
| avatar | `convoai-restapi/start-agent.md` (`avatar`) | - |

Routing: [README.md](README.md) for architecture → [sample-repos.md](sample-repos.md) if sample-aligned → REST endpoint docs for the specific operation.

### Debugging

Start from [common-errors.md](common-errors.md). Fetch endpoint docs only for the failing operation.
If provider-specific, run a partial provider check using [quickstart.md](quickstart.md) supported-provider lists.

### Ops / Hardening

- Auth → [credentials-and-auth.md](../general/credentials-and-auth.md)
- Tokens → [token-server](../token-server/README.md)
- Architecture → [README.md](README.md)

## Step 3: Ask Only Targeted Questions

Minimum questions to unblock the specific request. Do not reconfirm unrelated stages.

Partial preflight: validate only the touched scope (auth issue → auth only, TTS issue → TTS only).
Escalate to full quickstart only if there's no real working baseline after all.
