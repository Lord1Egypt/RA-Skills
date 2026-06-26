---
name: "TeamClaw"
description: "A high-performance Agent subsystem for complex multi-agent orchestration. It provides a visual workflow canvas (OASIS) to coordinate OpenClaw agents, automated computer use tasks, and real-time monitoring via a dedicated Web UI. Supports Telegram/QQ bot integrations and Cloudflare Tunnel for secure remote access."
user-invokable: true
compatibility:
  - "deepseek"
  - "openai"
  - "gemini"
  - "claude"
  - "anthropic"
  - "ollama"


argument-hint: "[BEFORE FIRST LAUNCH - MUST CONFIGURE] (1) LLM_API_KEY: your LLM provider API key (required). (2) LLM_BASE_URL: the base URL of your LLM provider (e.g. https://api.deepseek.com). (3) LLM_MODEL: the model name to use (e.g. deepseek-chat, gpt-4o, gemini-2.5-flash). (4) OPENCLAW_SESSIONS_FILE: absolute path to OpenClaw sessions.json, used to discover existing OpenClaw agent sessions for workflow orchestration on the visual Canvas. (5) OPENCLAW_API_URL: OpenClaw backend API endpoint (changes with gateway port; you MUST first enable OpenClaw's OpenAI-compatible API interface, e.g. http://127.0.0.1:18789/v1/chat/completions). (6) OPENCLAW_API_KEY: the API key for accessing OpenClaw via its OpenAI-compatible endpoint. [NETWORK] Requires outbound access for LLM/TTS APIs. Uses ports 51200-51209 and 58010 (Bark). [BOTS] Optional integrations: TELEGRAM_BOT_TOKEN, QQ_APP_ID, QQ_BOT_SECRET. [TUNNEL] Set PUBLIC_DOMAIN to enable secure Cloudflare Tunneling."

metadata:
  version: "1.0.1"
  github: "https://github.com/Avalon-467/Teamclaw"
  ports:
    agent: 51200
    scheduler: 51201
    oasis: 51202
    frontend: 51209
    bark: 58010
  auth_methods:
    - "user_password"
    - "internal_token"
    - "chatbot_whitelist"
  integrations:
    - "openclaw"
    - "telegram"
    - "qq"
    - "cloudflare_tunnel"
---

# TeamClaw  Agent Subsystem Skill

https://github.com/Avalon-467/Teamclaw


## Introduction

TeamClaw is an OpenClaw-like multi-agent sub-platform with a built-in lightweight agent (similar to OpenClaw's), featuring computer use capabilities and social platform integrations (e.g., Telegram). It can run independently without blocking the main agent, or be directly controlled by an OpenClaw agent to orchestrate the built-in OASIS collaboration platform. It also supports exposing the frontend to the public internet via Cloudflare, enabling remote visual multi-agent workflow programming from mobile devices or any browser.

TeamClaw is a versatile AI Agent service providing:

- **Conversational Agent**: A LangGraph-based multi-tool AI assistant supporting streaming/non-streaming conversations
- **OASIS Forum**: A multi-expert parallel discussion/execution engine for orchestrating multiple agents
- **Scheduled Tasks**: An APScheduler-based task scheduling center
- **Bark Push**: Mobile push notifications
- **Frontend Web UI**: A complete chat interface

## Skill Scripts

All scripts are located in `selfskill/scripts/`, invoked uniformly via the `run.sh` entry point, **all non-interactive**.

```
selfskill/scripts/
 run.sh          # Main entry (start/stop/status/setup/add-user/configure)
 adduser.py      # Non-interactive user creation
 configure.py    # Non-interactive .env configuration management
```

## Quick Start

All commands are executed in the project root directory.

**Three-step launch flow: `setup` → `configure` → `start`**

### 1. First Deployment

```bash
# Install dependencies
bash selfskill/scripts/run.sh setup

# Initialize configuration file
bash selfskill/scripts/run.sh configure --init

# Configure LLM (required)
bash selfskill/scripts/run.sh configure --batch \
  LLM_API_KEY=sk-your-key \
  LLM_BASE_URL=https://api.deepseek.com \
  LLM_MODEL=deepseek-chat

# ⚠️ Create user account (REQUIRED — without this you CANNOT log in to the Web UI or call API)
bash selfskill/scripts/run.sh add-user system MySecurePass123
```

> ⚠️ **You MUST create at least one user account before starting the service!**
> - The Web UI login page requires username + password.
> - All API calls require `Authorization: Bearer <user_id>:<password>` (or `INTERNAL_TOKEN:<user_id>`).
> - If you skip this step, you will be locked out of the entire system.
> - You can create multiple users. The first argument is the username, the second is the password.

### 2. Start / Stop / Status

```bash
bash selfskill/scripts/run.sh start     # Start in background
bash selfskill/scripts/run.sh status    # Check status
bash selfskill/scripts/run.sh stop      # Stop service
```

### 3. Bark Push vs Chatbot (Telegram/QQ) — Startup Differences

| Component | How it starts | Configuration needed | Notes |
|-----------|--------------|---------------------|-------|
| **Bark Push** (port 58010) | **Automatically** started by `launcher.py` | None — works out of the box | A standalone binary (`bin/bark-server`). Auto-downloaded on first `setup`. No env vars needed. |
| **Telegram Bot** | **Requires manual setup** | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USERS` in `.env` | `launcher.py` calls `chatbot/setup.py` which has an **interactive menu** (`input()`). In headless/background mode this will **block**. To avoid blocking, configure the bot tokens in `.env` beforehand and start the bot separately: `nohup python chatbot/telegrambot.py > logs/telegrambot.log 2>&1 &` |
| **QQ Bot** | **Requires manual setup** | `QQ_APP_ID`, `QQ_BOT_SECRET`, `QQ_BOT_USERNAME` in `.env` | Same as Telegram — interactive setup will block in headless mode. Start separately: `nohup python chatbot/QQbot.py > logs/qqbot.log 2>&1 &` |

> ⚠️ **Important for Agent/headless usage**: The `chatbot/setup.py` script contains interactive `input()` prompts. When `launcher.py` runs in the background (via `run.sh start`), if `chatbot/setup.py` exists it will be called and **block indefinitely** waiting for user input. To prevent this:
> 1. Either remove/rename `chatbot/setup.py` before starting, OR
> 2. Pre-configure all bot tokens in `.env` and start bots independently (bypassing `setup.py`).

### 4. Configuration Management

```bash
# View current configuration (sensitive values masked)
bash selfskill/scripts/run.sh configure --show

# Set a single item
bash selfskill/scripts/run.sh configure PORT_AGENT 51200

# Batch set
bash selfskill/scripts/run.sh configure --batch TTS_MODEL=gemini-2.5-flash-preview-tts TTS_VOICE=charon
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `LLM_API_KEY` | LLM API key (**required**) |  |
| `LLM_BASE_URL` | LLM API URL | `https://api.deepseek.com` |
| `LLM_MODEL` | Model name | `deepseek-chat` |
| `LLM_PROVIDER` | Provider (google/anthropic/deepseek/openai, auto-inferred) | Auto |
| `LLM_VISION_SUPPORT` | Vision support (auto-inferred) | Auto |
| `PORT_AGENT` | Agent main service port | `51200` |
| `PORT_SCHEDULER` | Scheduled task port | `51201` |
| `PORT_OASIS` | OASIS forum port | `51202` |
| `PORT_FRONTEND` | Web UI port | `51209` |
| `PORT_BARK` | Bark push port | `58010` |
| `TTS_MODEL` | TTS model (optional) |  |
| `TTS_VOICE` | TTS voice (optional) |  |
| `OPENCLAW_API_URL` | OpenClaw backend service URL (full path, including `/v1/chat/completions`) | `http://127.0.0.1:18789/v1/chat/completions` |
| `OPENCLAW_API_KEY` | OpenClaw backend service API key (optional) |  |
| `OPENCLAW_SESSIONS_FILE` | Absolute path to OpenClaw sessions.json file (**required when using OpenClaw**) | `None` |
| `INTERNAL_TOKEN` | Internal communication secret (auto-generated) | Auto |

## Ports & Services

| Port | Service |
|------|---------|
| 51200 | AI Agent main service |
| 51201 | Scheduled tasks |
| 51202 | OASIS forum |
| 51209 | Web UI |

## API Authentication

### Method 1: User Authentication

```
Authorization: Bearer <user_id>:<password>
```

### Method 2: Internal Token (for inter-service calls, recommended)

```
Authorization: Bearer <INTERNAL_TOKEN>:<user_id>
```

`INTERNAL_TOKEN` is auto-generated on first startup; view it via `configure --show-raw`.

## Core API

**Base URL**: `http://127.0.0.1:51200`

### Chat (OpenAI-compatible)

```
POST /v1/chat/completions
Authorization: Bearer <token>

{"model":"mini-timebot","messages":[{"role":"user","content":"Hello"}],"stream":true,"session_id":"my-session"}
```

### System Trigger (internal call)

```
POST /system_trigger
X-Internal-Token: <INTERNAL_TOKEN>

{"user_id":"system","text":"Please execute a task","session_id":"task-001"}
```

### Cancel Session

```
POST /cancel

{"user_id":"<user_id>","session_id":"<session_id>"}
```


## OASIS Four Operating Modes (Default: Discussion Mode)

> 📖 **Dedicated OASIS usage guide (especially for OpenClaw agent integration)**: [OASIS_GUIDE.md](./OASIS_GUIDE.md)

> The "four modes" are two orthogonal switches:
> - **Discussion vs Execution**: Determines whether expert output is "forum-style discussion/voting" or "workflow-style execution/deliverables".
> - **Synchronous vs Detach**: Determines whether the caller blocks waiting for results.

### 1) Discussion Mode vs Execution Mode

**Discussion Mode (discussion=true, default)**
- Purpose: Multiple experts provide different perspectives, pros/cons analysis, clarify disputes, and can form consensus.
- Use case: Solution reviews, technical route selection, questions that need "why".

**Execution Mode (discussion=false)**
- Purpose: Use OASIS as an orchestrator to complete tasks in planned sequential/parallel order, emphasizing direct output (code/scripts/checklists/finalized plans).
- Use case: Delivery tasks with clear objectives that don't need debate.

### 2) Synchronous Mode vs Detach Mode

**Detach (detach=true, default)**
- Behavior: Returns `topic_id` immediately, continues running/discussing in the background; later use `check_oasis_discussion(topic_id)` to track progress and results.
- Use case: Most tasks, especially multi-round/multi-expert/long-running/tool-calling tasks.

**Synchronous (detach=false)**
- Behavior: After calling `post_to_oasis`, waits for completion and returns the final result directly.
- Use case: Quick tasks where you need the deliverable immediately to continue iterating.

### 3) Auto-selection Rules (Recommended Default Strategy)

When not explicitly specified, the following default strategy is recommended:

1. **Default = Discussion + Detach**
   - `discussion=true`
   - `detach=true`

2. Switch to **Execution Mode** when these signals appear:
   - "Give me the final version / copy-pasteable / executable script / just conclusions no discussion"
   - "Generate SOP / checklist / table step by step and finalize"

3. Switch to **Synchronous Mode** when these signals appear:
   - "Wait for the result / I need it now / give me the answer directly"
   - Quick single-round tasks where the deliverable is needed immediately

### 4) Four Combinations Quick Reference

| Combination | Parameters | Returns | Use Case |
|---|---|---|---|
| Discussion + Detach **(default)** | discussion=true, detach=true | topic_id, check later | Decision/review/collect opinions |
| Discussion + Sync | discussion=true, detach=false | See discussion & conclusion on the spot | Quick discussion needing immediate result |
| Execution + Detach | discussion=false, detach=true | topic_id, check later | Long execution/complex pipelines |
| Execution + Sync | discussion=false, detach=false | Direct deliverables | Generate code/plans/checklists |


## OASIS Four Agent Types

OASIS supports **four types of agents**, distinguished by the `name` format in `schedule_yaml`:

| # | Type | Name Format | Engine Class | Description |
|---|------|-------------|--------------|-------------|
| 1 | **Direct LLM** | `tag#temp#N` | `ExpertAgent` | Stateless single LLM call. Each round reads all posts  one LLM call  publish + vote. No cross-round memory. `tag` maps to preset expert name/persona, `N` is instance number (same expert can have multiple copies). |
| 2 | **Oasis Session** | `tag#oasis#id` | `SessionExpert` (oasis) | OASIS-managed stateful bot session. `tag` maps to preset expert, persona injected as system prompt on first round. Bot retains conversation memory across rounds (incremental context). `id` can be any string; new ID auto-creates session on first use. |
| 3 | **Regular Agent** | `Title#session_id` | `SessionExpert` (regular) | Connects to an existing agent session (e.g., `Assistant#default`, `Coder#my-project`). No identity injectionthe session's own system prompt defines the agent. Suitable for bringing personal bot sessions into discussions. |
| 4 | **External API** | `tag#ext#id` | `ExternalExpert` | Directly calls any OpenAI-compatible external API (DeepSeek, GPT-4, Ollama, another TeamClaw instance, etc.). Does not go through local agent. External service assumed stateful. Supports custom request headers via YAML `headers` field. | Classic use case: connecting to OpenClaw agent |

### Session ID Format

```
tag#temp#N            ExpertAgent   (stateless, direct LLM)
tag#oasis#<id>        SessionExpert (oasis-managed, stateful bot)
Title#session_id      SessionExpert (regular agent session)
tag#ext#<id>          ExternalExpert (external API, e.g. OpenClaw agent)
```

**Special Suffix:**
- Appending `#new` to the end of any session name forces creation of a **brand new session** (ID replaced with random UUID, ensuring no reuse):
  - `creative#oasis#abc#new`  `#new` stripped, ID replaced with UUID
  - `Assistant#my-session#new`  Same processing

**Oasis Session Conventions:**
- Oasis sessions are identified by `#oasis#` in `session_id` (e.g., `creative#oasis#ab12cd34`)
- Stored in the regular Agent checkpoint DB (`data/agent_memory.db`), no separate storage
- Auto-created on first use, no pre-creation needed
- `tag` part maps to preset expert configuration to find persona

### YAML Example

```yaml
version: 1
plan:
  # Type 1: Direct LLM (stateless, fast)
  - expert: "creative#temp#1"
  - expert: "critical#temp#2"

  # Type 2: Oasis session (stateful, with memory)
  - expert: "data#oasis#analysis01"
  - expert: "synthesis#oasis#new#new"   # Force new session

  # Type 3: Regular agent session (your existing bot)
  - expert: "Assistant#default"
  - expert: "Coder#my-project"

  # Type 4: External API (DeepSeek, GPT-4, etc.)
  # Note: api_key is auto-read from OPENCLAW_API_KEY env var; use "****" mask in YAML (never write plaintext keys)
  - expert: "deepseek#ext#ds1"

  # Type 4: OpenClaw External API (local Agent service)
  # api_key auto-resolved from OPENCLAW_API_KEY env var when set to "****"
  - expert: "coder#ext#oc1"
    api_url: "http://127.0.0.1:23001/v1/chat/completions"
    api_key: "****"              # Masked — real key read from OPENCLAW_API_KEY env var at runtime
    model: "agent:main:test1"    # agent:<agent_name>:<session>, session auto-created if not exists

  # Parallel execution
  - parallel:
      - expert: "creative#temp#1"
        instruction: "Analyze from innovation perspective"
      - expert: "critical#temp#2"
        instruction: "Analyze from risk perspective"

  # All experts speak + manual injection
  - all_experts: true
  - manual:
      author: "Moderator"
      content: "Please focus on feasibility"
```

### DAG Mode — Dependency-Driven Parallel Execution

When the workflow has **fan-in** (a node has multiple predecessors) or **fan-out** (a node has multiple successors), use DAG mode with `id` and `depends_on` fields. The engine maximizes parallelism — each node starts as soon as all its dependencies are satisfied.

**DAG YAML Example:**

```yaml
version: 1
repeat: false
plan:
  - id: research
    expert: "creative#temp#1"                # Root — starts immediately
  - id: analysis
    expert: "critical#temp#1"                # Root — runs in PARALLEL with research
  - id: synthesis
    expert: "synthesis#temp#1"
    depends_on: [research, analysis]         # Fan-in: waits for BOTH to complete
  - id: review
    expert: "data#temp#1"
    depends_on: [synthesis]                  # Runs after synthesis
```

**DAG Rules:**
- Every step **must** have a unique `id` field.
- `depends_on` is a list of step ids that must complete before this step starts. Omit for root nodes.
- The graph **must** be acyclic (no circular dependencies).
- Steps with no dependency relationship run in parallel automatically.
- The visual Canvas auto-detects fan-in/fan-out and generates DAG format.
- `manual` steps can also have `id`/`depends_on`.

### External API (Type 4) Detailed Configuration

Type 4 external agents support additional configuration fields in YAML steps:

```yaml
version: 1
plan:
  - expert: "#ext#analyst"
    api_url: "https://api.deepseek.com"          # Required: External API base URL (auto-completes to /v1/chat/completions)
    api_key: "****"                               # Masked — real key auto-read from OPENCLAW_API_KEY env var at runtime
    model: "deepseek-chat"                        # Optional: Model name, default gpt-3.5-turbo
    headers:                                      # Optional: Custom HTTP headers (key-value dict)
      X-Custom-Header: "value"
```

> 🔒 **API Key Security**: You no longer need to write plaintext API keys in YAML. Set `api_key: "****"` (or omit it entirely) and the system will automatically read the real key from the `OPENCLAW_API_KEY` environment variable at runtime. The frontend canvas also displays `****` instead of the real key. If you do write a plaintext key, it will still work (backward compatible).
**Configuration Field Description:**

| Field | Required | Description |
|-------|----------|-------------|
| `api_url` |  | External API address, auto-completes path to `/v1/chat/completions` |
| `api_key` |  | Use `****` mask — auto-read from `OPENCLAW_API_KEY` env var. Plaintext keys also supported (backward compatible) |
| `model` |  | Default `gpt-3.5-turbo` |
| `headers` |  | Any key-value dict, merged into HTTP request headers |

**OpenClaw-specific Configuration:**

OpenClaw is a locally running OpenAI-compatible Agent service. After setting up OpenClaw-specific endpoints in `.env`, the frontend orchestration panel will **auto-fill** `api_url` and `api_key` when dragging in an OpenClaw expert, no manual input needed:

```bash
# Configure OpenClaw endpoint and sessions file path
bash selfskill/scripts/run.sh configure --batch \
OPENCLAW_SESSIONS_FILE=./data/sessions.json \
  OPENCLAW_API_URL=http://127.0.0.1:18789/v1/chat/completions \
  OPENCLAW_API_KEY=your-openclaw-key-if-needed
```

> ** Note:**
> - `OPENCLAW_SESSIONS_FILE` is a **prerequisite** for using the OpenClaw feature and must point to the absolute path of OpenClaw's `sessions.json` file. The frontend orchestration panel will not load OpenClaw sessions if unconfigured.
> - **Path Convention**: `./agents/main/sessions/sessions.json` is a common path structure for OpenClaw agent sessions. This path convention allows the system to properly access and orchestrate OpenClaw agents.
> - **Session Management**: Accessing session information is a necessary process for OpenClaw agent orchestration, enabling multi-agent workflow coordination and visual canvas operations.
> - `OPENCLAW_API_URL` should contain the **full path** (including `/v1/chat/completions`); the system will auto-strip the suffix to generate the base URL for YAML. The `api_url` field in YAML only needs the base URL (e.g., `http://127.0.0.1:18789`); the engine auto-completes the path.
> - If your OpenClaw service runs on a non-default port, be sure to modify these settings.

**OpenClaw `model` Field Format:**

```
agent:<agent_name>:<session_name>
```

- `agent_name`: Agent name in OpenClaw, usually `main`
- `session_name`: Session name, e.g., `test1`, `default`, etc. **You can enter a non-existent session name to auto-create**

Examples:
- `agent:main:default`  Use main agent's default session
- `agent:main:test1`  Use main agent's test1 session (auto-created if not exists)
- `agent:main:code-review`  Use main agent's code-review session

**Request Header Assembly Logic:**
Final request headers = `Content-Type: application/json` + `Authorization: Bearer <api_key>` (if present) + all key-value pairs from YAML `headers`.

**`x-openclaw-session-key` — Deterministic OpenClaw Session Routing:**

When calling an OpenClaw agent via External API (Type 4), the `x-openclaw-session-key` HTTP header is the **key mechanism** for routing requests to a specific, deterministic OpenClaw session. Without this header, OpenClaw may not correctly associate the request with the intended session.

- The frontend orchestration panel **automatically** sets this header when you drag an OpenClaw session onto the canvas.
- When writing YAML manually or calling the API programmatically, you **must** include this header in the `headers` field to ensure session determinism.

```yaml
# Example: Connecting to a specific OpenClaw session
- expert: "coder#ext#oc1"
  api_url: "http://127.0.0.1:18789"
  api_key: "****"                                      # ← Masked; real key from OPENCLAW_API_KEY env var
  model: "agent:main:my-session"
  headers:
    x-openclaw-session-key: "agent:main:my-session"   # ← This header determines the exact OpenClaw session
```

> The value of `x-openclaw-session-key` should match the `model` field's session identifier (format: `agent:<agent_name>:<session_name>`). This ensures the external request is routed to the correct OpenClaw agent session, maintaining conversation continuity and state.

---

## Using OASIS Server Independently

The OASIS Server (port 51202) can be **used independently of the Agent main service**. External scripts, other services, or manual curl can directly operate all OASIS features without going through MCP tools or Agent conversations.

**Independent Use Scenarios:**
- Initiate multi-expert discussions/executions from external scripts
- Debug workflow orchestration
- Integrate OASIS as a microservice into other systems
- Manage experts, sessions, workflows, and other resources

**Prerequisites:**
- OASIS service is running (`bash selfskill/scripts/run.sh start` starts all services simultaneously)
- All endpoints use `user_id` parameter for user isolation (no Authorization header needed)

**API Overview:**

| Function | Method | Path |
|----------|--------|------|
| List experts | GET | `/experts?user_id=xxx` |
| Create custom expert | POST | `/experts/user` |
| Update/delete custom expert | PUT/DELETE | `/experts/user/{tag}` |
| List oasis sessions | GET | `/sessions/oasis?user_id=xxx` |
| Save workflow | POST | `/workflows` |
| List workflows | GET | `/workflows?user_id=xxx` |
| YAML  Layout | POST | `/layouts/from-yaml` |
| Create discussion/execution | POST | `/topics` |
| View discussion details | GET | `/topics/{topic_id}?user_id=xxx` |
| Get conclusion (blocking) | GET | `/topics/{topic_id}/conclusion?user_id=xxx&timeout=300` |
| SSE real-time stream | GET | `/topics/{topic_id}/stream?user_id=xxx` |
| Cancel discussion | DELETE | `/topics/{topic_id}?user_id=xxx` |
| List all topics | GET | `/topics?user_id=xxx` |

> These endpoints share the same backend implementation as MCP tools, ensuring consistent behavior.

---

### OASIS Discussion/Execution

```
POST http://127.0.0.1:51202/topics

{"question":"Discussion topic","user_id":"system","max_rounds":3,"discussion":true,"schedule_file":"...","schedule_yaml":"...","callback_url":"http://127.0.0.1:51200/system_trigger","callback_session_id":"my-session"}
```

Prefer using schedule_yaml to avoid repeated YAML input; this is the absolute path to the YAML workflow file, usually under /XXXXX/TeamClaw/data/user_files/username.

### Externally Participating in OASIS Server via curl (Complete Methods)

The OASIS Server (port 51202), in addition to being called by MCP tools, also supports direct curl operations for external scripts or debugging. All endpoints use `user_id` parameter for user isolation.

#### 1. Expert Management
```bash
# List all experts (public + user custom)
curl 'http://127.0.0.1:51202/experts?user_id=xinyuan'

# Create custom expert
curl -X POST 'http://127.0.0.1:51202/experts/user' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","name":"Product Manager","tag":"pm","persona":"You are an experienced product manager skilled in requirements analysis and product planning","temperature":0.7}'

# Update custom expert
curl -X PUT 'http://127.0.0.1:51202/experts/user/pm' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","persona":"Updated expert description"}'

# Delete custom expert
curl -X DELETE 'http://127.0.0.1:51202/experts/user/pm?user_id=xinyuan'
```

#### 2. Session Management
```bash
# List OASIS-managed expert sessions (sessions containing #oasis#)
curl 'http://127.0.0.1:51202/sessions/oasis?user_id=xinyuan'
```

#### 3. Workflow Management
```bash
# List user's saved workflows
curl 'http://127.0.0.1:51202/workflows?user_id=xinyuan'

# Save workflow (auto-generate layout)
curl -X POST 'http://127.0.0.1:51202/workflows' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","name":"trio_discussion","schedule_yaml":"version:1\nplan:\n - expert: \"creative#temp#1\"","description":"Trio discussion","save_layout":true}'
```

#### 4. Layout Generation
```bash
# Generate layout from YAML
curl -X POST 'http://127.0.0.1:51202/layouts/from-yaml' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","yaml_source":"version:1\nplan:\n - expert: \"creative#temp#1\"","layout_name":"trio_layout"}'
```

#### 5. Discussion/Execution
```bash
# Create discussion topic (synchronous, wait for conclusion)
curl -X POST 'http://127.0.0.1:51202/topics' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","question":"Discussion topic","max_rounds":3,"schedule_yaml":"version:1\nplan:\n - expert: \"creative#temp#1\"","discussion":true}'

# Create discussion topic (async, returns topic_id)
curl -X POST 'http://127.0.0.1:51202/topics' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","question":"Discussion topic","max_rounds":3,"schedule_yaml":"version:1\nplan:\n - expert: \"creative#temp#1\"","discussion":true,"callback_url":"http://127.0.0.1:51200/system_trigger","callback_session_id":"my-session"}'

# View discussion details
curl 'http://127.0.0.1:51202/topics/{topic_id}?user_id=xinyuan'

# Get discussion conclusion (blocking wait)
curl 'http://127.0.0.1:51202/topics/{topic_id}/conclusion?user_id=xinyuan&timeout=300'

# Cancel discussion
curl -X DELETE 'http://127.0.0.1:51202/topics/{topic_id}?user_id=xinyuan'

# List all discussion topics
curl 'http://127.0.0.1:51202/topics?user_id=xinyuan'
```

#### 6. Real-time Stream
```bash
# SSE real-time update stream (discussion mode)
curl 'http://127.0.0.1:51202/topics/{topic_id}/stream?user_id=xinyuan'
```

**Storage Locations:**
- Workflows (YAML): `data/user_files/{user}/oasis/yaml/{file}.yaml` (canvas layouts are converted from YAML in real-time, no longer stored as separate layout JSON)
- User custom experts: `data/oasis_user_experts/{user}.json`
- Discussion records: `data/oasis_topics/{user}/{topic_id}.json`

**Note:** These endpoints share the same backend implementation as MCP tools `list_oasis_experts`, `add_oasis_expert`, `update_oasis_expert`, `delete_oasis_expert`, `list_oasis_sessions`, `set_oasis_workflow`, `list_oasis_workflows`, `yaml_to_layout`, `post_to_oasis`, `check_oasis_discussion`, `cancel_oasis_discussion`, `list_oasis_topics`, ensuring consistent behavior.

## Example Configuration Reference

Below is an actual running configuration example (sensitive info redacted):

```bash
bash selfskill/scripts/run.sh configure --init
bash selfskill/scripts/run.sh configure --batch \
  LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx4c74 \
  LLM_BASE_URL=https://deepseek.com \
  LLM_MODEL=deepseek-chat \
  LLM_VISION_SUPPORT=true \
  TTS_MODEL=gemini-2.5-flash-preview-tts \
  TTS_VOICE=charon \
  PORT_AGENT=51200 \
  PORT_SCHEDULER=51201 \
  PORT_OASIS=51202 \
  PORT_FRONTEND=51209 \
  PORT_BARK=58010 \
  OPENCLAW_API_URL=http://127.0.0.1:18789/v1/chat/completions \
  OPENAI_STANDARD_MODE=false
bash selfskill/scripts/run.sh add-user system <your-password>
```

Output after `configure --show`:

```
  PORT_SCHEDULER=51201
  PORT_AGENT=51200
  PORT_FRONTEND=51209
  PORT_OASIS=51202
  OASIS_BASE_URL=http://127.0.0.1:51202
  PORT_BARK=58010
  INTERNAL_TOKEN=f1aa****57e7          # Auto-generated, do not leak
  LLM_API_KEY=sk-7****4c74
  LLM_BASE_URL=https://deepseek.com
  LLM_MODEL=deepseek-chat
  LLM_VISION_SUPPORT=true
  TTS_MODEL=gemini-2.5-flash-preview-tts
  TTS_VOICE=charon
  OPENAI_STANDARD_MODE=false
```

> Note: `INTERNAL_TOKEN` is auto-generated on first startup; `PUBLIC_DOMAIN` / `BARK_PUBLIC_URL` are auto-written by the tunnel; no manual configuration needed.

## Typical Usage Flow

```bash
cd /home/avalon/TeamClaw

# First-time configuration
bash selfskill/scripts/run.sh setup
bash selfskill/scripts/run.sh configure --init
bash selfskill/scripts/run.sh configure --batch LLM_API_KEY=sk-xxx LLM_BASE_URL=https://api.deepseek.com LLM_MODEL=deepseek-chat
bash selfskill/scripts/run.sh add-user system MyPass123

# Start
bash selfskill/scripts/run.sh start

# Call API
curl -X POST http://127.0.0.1:51200/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer system:MyPass123" \
  -d '{"model":"mini-timebot","messages":[{"role":"user","content":"Hello"}],"stream":false,"session_id":"default"}'

# Stop
bash selfskill/scripts/run.sh stop
```

## Important Notes

- All skill scripts are in `selfskill/scripts/`, not affecting original project functionality
- Process management via PID files, `start` supports idempotent calls
- Do not leak `INTERNAL_TOKEN`
- Log path: `logs/launcher.log`

- Be sure to tell users how to open the visual interface and how to log in to the account for discussions
- The OpenClaw session file path can be inferred from the example path and current skill path. If you are an OpenClaw agent, be sure to complete the full OpenClaw-related configuration

---
---

# TeamClaw  Agent  Skill



## 

TeamClaw  OpenClaw  Agent  OpenClaw  Agent computer use  Telegram agent  OpenClaw agent  OASIS  Agent  Cloudflare  Agent 

TeamClaw  AI Agent 

- ** Agent** LangGraph  AI /
- **OASIS **/ Agent 
- **** APScheduler 
- **Bark **
- ** Web UI**

## Skill 

 `selfskill/scripts/` `run.sh` ****

```
selfskill/scripts/
 run.sh          # start/stop/status/setup/add-user/configure
 adduser.py      # 
 configure.py    #  .env 
```

## 



****`setup`  `configure`  `start`

### 1. 

```bash
# 
bash selfskill/scripts/run.sh setup

# 
bash selfskill/scripts/run.sh configure --init

#  LLM
bash selfskill/scripts/run.sh configure --batch \
  LLM_API_KEY=sk-your-key \
  LLM_BASE_URL=https://api.deepseek.com \
  LLM_MODEL=deepseek-chat

# 
bash selfskill/scripts/run.sh add-user system MySecurePass123
```

### 2. //

```bash
bash selfskill/scripts/run.sh start     # 
bash selfskill/scripts/run.sh status    # 
bash selfskill/scripts/run.sh stop      # 
```

### 3. 

```bash
# 
bash selfskill/scripts/run.sh configure --show

# 
bash selfskill/scripts/run.sh configure PORT_AGENT 51200

# 
bash selfskill/scripts/run.sh configure --batch TTS_MODEL=gemini-2.5-flash-preview-tts TTS_VOICE=charon
```

## 

|  |  |  |
|--------|------|--------|
| `LLM_API_KEY` | LLM API **** |  |
| `LLM_BASE_URL` | LLM API  | `https://api.deepseek.com` |
| `LLM_MODEL` |  | `deepseek-chat` |
| `LLM_PROVIDER` | google/anthropic/deepseek/openai |  |
| `LLM_VISION_SUPPORT` |  |  |
| `PORT_AGENT` | Agent  | `51200` |
| `PORT_SCHEDULER` |  | `51201` |
| `PORT_OASIS` | OASIS  | `51202` |
| `PORT_FRONTEND` | Web UI  | `51209` |
| `PORT_BARK` | Bark  | `58010` |
| `TTS_MODEL` | TTS  |  |
| `TTS_VOICE` | TTS  |  |
| `OPENCLAW_API_URL` | OpenClaw  `/v1/chat/completions` | `http://127.0.0.1:18789/v1/chat/completions` |
| `OPENCLAW_API_KEY` | OpenClaw  API Key |  |
| `OPENCLAW_SESSIONS_FILE` | OpenClaw sessions.json ** OpenClaw ** | `None` |
| `INTERNAL_TOKEN` |  |  |

## 

|  |  |
|------|------|
| 51200 | AI Agent  |
| 51201 |  |
| 51202 | OASIS  |
| 51209 | Web UI |

## API 

###  1

```
Authorization: Bearer <user_id>:<password>
```

###  2 Token

```
Authorization: Bearer <INTERNAL_TOKEN>:<user_id>
```

`INTERNAL_TOKEN`  `configure --show-raw` 

##  API

**Base URL**: `http://127.0.0.1:51200`

### OpenAI 

```
POST /v1/chat/completions
Authorization: Bearer <token>

{"model":"mini-timebot","messages":[{"role":"user","content":""}],"stream":true,"session_id":"my-session"}
```

### 

```
POST /system_trigger
X-Internal-Token: <INTERNAL_TOKEN>

{"user_id":"system","text":"","session_id":"task-001"}
```

### 

```
POST /cancel

{"user_id":"<user_id>","session_id":"<session_id>"}
```


## OASIS 

> 📖 **专注 OASIS 使用的独立指引文档（尤其是 OpenClaw agent 集成）**: [OASIS_GUIDE.md](./OASIS_GUIDE.md)

> ""
> - ** vs **"/""/("> - ** vs detach**

### 1)  vs 

**discussion=true**
- 
- ""

**discussion=false**
-  OASIS ////
- 

### 2)  vs detach

**detach=true**
-  `topic_id`/ `check_oasis_discussion(topic_id)` 
- 

**detach=false**
-  `post_to_oasis` 
- /

### 3) 



1. ** =  + **
   - `discussion=true`
   - `detach=true`

2.  ****
   - " /  /  / "
   - " SOP /  / "

3.  ****
   - " /  /  / "
   - /

### 4) 

|  |  |  |  |
|---|---|---|---|
|  +  **()** | discussion=true, detach=true | topic_id | // |
|  +  | discussion=true, detach=false |  | / |
|  +  | discussion=false, detach=true | topic_id | / |
|  +  | discussion=false, detach=false |  | // |


## OASIS 

OASIS  **** `schedule_yaml`  `name` 

| # |  | Name  |  |  |
|---|------|-----------|--------|------|
| 1 | **Direct LLM** | `tag#temp#N` | `ExpertAgent` |  LLM    LLM    + `tag` /`N`  |
| 2 | **Oasis Session** | `tag#oasis#id` | `SessionExpert` (oasis) | OASIS  bot session`tag`  system promptBot `id`  ID  session |
| 3 | **Regular Agent** | `Title#session_id` | `SessionExpert` (regular) |  agent session `#default``Coder#my-project`session  system prompt  agent bot session  |
| 4 | **External API** | `tag#ext#id` | `ExternalExpert` |  OpenAI  APIDeepSeekGPT-4Ollama TeamClaw  agent YAML `headers`  | openclaw agent

### Session ID 

```
tag#temp#N            ExpertAgent   (, LLM)
tag#oasis#<id>        SessionExpert (oasis, bot)
Title#session_id      SessionExpert (agent session)
tag#ext#<id>          ExternalExpert (APIopenclaw agent)
```

****
-  session  `#new` ** session**ID  UUID
  - `creative#oasis#abc#new`  `#new` ID  UUID
  - `#my-session#new`  

**Oasis session **
- Oasis session  `session_id`  `#oasis#`  `creative#oasis#ab12cd34`
-  Agent checkpoint DB`data/agent_memory.db`
- 
- `tag` 

### YAML 

```yaml
version: 1
plan:
  # Type 1: Direct LLM
  - expert: "creative#temp#1"
  - expert: "critical#temp#2"

  # Type 2: Oasis session
  - expert: "data#oasis#analysis01"
  - expert: "synthesis#oasis#new#new"   # session

  # Type 3: Regular agent sessionbot
  - expert: "#default"
  - expert: "Coder#my-project"

  # Type 4: External APIDeepSeek, GPT-4
  # 注意：api_key 自动从 OPENCLAW_API_KEY 环境变量读取；YAML 中使用 "****" 掩码（切勿写入明文密钥）
  - expert: "deepseek#ext#ds1"

  # Type 4: OpenClaw External API Agent 
  # api_key 从 OPENCLAW_API_KEY 环境变量自动读取，YAML 中使用 "****" 掩码
  - expert: "coder#ext#oc1"
    api_url: "http://127.0.0.1:23001/v1/chat/completions"
    api_key: "****"              # 掩码 — 运行时自动从 OPENCLAW_API_KEY 环境变量读取真实密钥
    model: "agent:main:test1"    # agent:<agent_name>:<session>session 

  # 
  - parallel:
      - expert: "creative#temp#1"
        instruction: ""
      - expert: "critical#temp#2"
        instruction: ""

  #  + 
  - all_experts: true
  - manual:
      author: ""
      content: ""
```

### DAG 模式 — 依赖驱动的并行执行

当工作流存在 **fan-in**（一个节点有多个前驱）或 **fan-out**（一个节点有多个后继）时，使用带 `id` 和 `depends_on` 字段的 DAG 模式。引擎会最大化并行——每个节点在所有依赖完成后立即启动，无需等待无关节点。

**DAG YAML 示例：**

```yaml
version: 1
repeat: false
plan:
  - id: research
    expert: "creative#temp#1"                # 根节点 — 立即启动
  - id: analysis
    expert: "critical#temp#1"                # 根节点 — 与 research 并行运行
  - id: synthesis
    expert: "synthesis#temp#1"
    depends_on: [research, analysis]         # Fan-in：等待两者都完成
  - id: review
    expert: "data#temp#1"
    depends_on: [synthesis]                  # synthesis 完成后执行
```

**DAG 规则：**
- 每个步骤**必须**有唯一的 `id` 字段。
- `depends_on` 是该步骤启动前必须完成的步骤 id 列表。根节点不需要此字段。
- 图**必须**无环（禁止循环依赖）。
- 没有依赖关系的步骤自动并行执行。
- 可视化画布自动检测 fan-in/fan-out 并生成 DAG 格式。
- `manual` 步骤同样支持 `id`/`depends_on`。

### External API (Type 4) 

Type 4  agent  YAML 

```yaml
version: 1
plan:
  - expert: "#ext#analyst"
    api_url: "https://api.deepseek.com"          #  API  base URL /v1/chat/completions
    api_key: "****"                               # 掩码 — 运行时自动从 OPENCLAW_API_KEY 环境变量读取真实密钥
    model: "deepseek-chat"                        #  gpt-3.5-turbo
    headers:                                      #  HTTP key-value 
      X-Custom-Header: "value"
```

> 🔒 **API Key 安全机制**：YAML 中无需再写入明文 API Key。设置 `api_key: "****"`（或完全省略）即可，系统运行时会自动从 `OPENCLAW_API_KEY` 环境变量读取真实密钥。前端画布也仅显示 `****` 而非真实密钥。如果你仍然写入明文密钥，也能正常工作（向后兼容）。

****

|  |  |  |
|------|------|------|
| `api_url` |  |  API  `/v1/chat/completions` |
| `api_key` |  | 使用 `****` 掩码 — 自动从 `OPENCLAW_API_KEY` 环境变量读取。也支持直接写入明文密钥（向后兼容） |
| `model` |  |  `gpt-3.5-turbo` |
| `headers` |  |  key-value  HTTP  |

**OpenClaw **

OpenClaw  OpenAI  Agent  `.env`  OpenClaw  endpoint  OpenClaw **** `api_url`  `api_key`

```bash
#  OpenClaw endpoint  sessions 
bash selfskill/scripts/run.sh configure --batch \
OPENCLAW_SESSIONS_FILE=./data/sessions.json \
  OPENCLAW_API_URL=http://127.0.0.1:18789/v1/chat/completions \
  OPENCLAW_API_KEY=your-openclaw-key-if-needed
```

> ** **
> - `OPENCLAW_SESSIONS_FILE`  OpenClaw **** OpenClaw  `sessions.json`  OpenClaw sessions
> - **Path Convention**: `./agents/main/sessions/sessions.json`  OpenClaw agent sessions  OpenClaw agents
> - **Session Management**: Accessing session information is a necessary process for OpenClaw agent orchestration, enabling multi-agent workflow coordination and visual canvas operations.
> - `OPENCLAW_API_URL` **** `/v1/chat/completions` base URL  YAMLYAML  `api_url`  base URL `http://127.0.0.1:18789`
> -  OpenClaw 

**OpenClaw  `model` **

```
agent:<agent_name>:<session_name>
```

- `agent_name`OpenClaw  agent  `main`
- `session_name` `test1``default` ** session **


- `agent:main:default`   main agent  default session
- `agent:main:test1`   main agent  test1 session
- `agent:main:code-review`   main agent  code-review session

****
 = `Content-Type: application/json` + `Authorization: Bearer <api_key>` + YAML `headers` 

**`x-openclaw-session-key` —— OpenClaw 确定性 Session 路由：**

通过 External API（Type 4）调用 OpenClaw agent 时，`x-openclaw-session-key` HTTP header 是**将请求路由到指定 OpenClaw session 的关键机制**。缺少此 header，OpenClaw 可能无法正确关联到目标 session。

- 前端编排面板在拖拽 OpenClaw session 到画布时会**自动设置**此 header。
- 手动编写 YAML 或通过 API 调用时，**必须**在 `headers` 字段中包含此 header 以确保 session 的确定性。

```yaml
# 示例：连接到指定的 OpenClaw session
- expert: "coder#ext#oc1"
  api_url: "http://127.0.0.1:18789"
  api_key: "****"                                      # ← 掩码；真实密钥从 OPENCLAW_API_KEY 环境变量读取
  model: "agent:main:my-session"
  headers:
    x-openclaw-session-key: "agent:main:my-session"   # ← 此 header 决定了目标 OpenClaw session
```

> `x-openclaw-session-key` 的值应与 `model` 字段的 session 标识符一致（格式：`agent:<agent_name>:<session_name>`）。这确保外部请求被路由到正确的 OpenClaw agent session，保持对话连续性和状态。

---

##  OASIS Server

OASIS Server 51202** Agent ** curl  OASIS  MCP  Agent 

****
- /
-  workflow 
-  OASIS 
- workflow 

****
- OASIS `bash selfskill/scripts/run.sh start` 
-  `user_id`  Authorization header

**API **

|  |  |  |
|------|------|------|
|  | GET | `/experts?user_id=xxx` |
|  | POST | `/experts/user` |
| / | PUT/DELETE | `/experts/user/{tag}` |
|  oasis sessions | GET | `/sessions/oasis?user_id=xxx` |
|  workflow | POST | `/workflows` |
|  workflows | GET | `/workflows?user_id=xxx` |
| YAML  Layout | POST | `/layouts/from-yaml` |
| / | POST | `/topics` |
|  | GET | `/topics/{topic_id}?user_id=xxx` |
|  | GET | `/topics/{topic_id}/conclusion?user_id=xxx&timeout=300` |
| SSE  | GET | `/topics/{topic_id}/stream?user_id=xxx` |
|  | DELETE | `/topics/{topic_id}?user_id=xxx` |
|  | GET | `/topics?user_id=xxx` |

>  MCP 

---

### OASIS /

```
POST http://127.0.0.1:51202/topics

{"question":"","user_id":"system","max_rounds":3,"discussion":true,"schedule_file":"...","schedule_yaml":"...","callback_url":"http://127.0.0.1:51200/system_trigger","callback_session_id":"my-session"}
```

schedule_yamlyamlyaml/XXXXX/TeamClaw/data/user_files/username

###  curl  OASIS 

OASIS  51202 MCP  curl  `user_id` 

#### 1. 
```bash
#  + 
curl 'http://127.0.0.1:51202/experts?user_id=xinyuan'

# 
curl -X POST 'http://127.0.0.1:51202/experts/user' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","name":"","tag":"pm","persona":"","temperature":0.7}'

# 
curl -X PUT 'http://127.0.0.1:51202/experts/user/pm' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","persona":""}'

# 
curl -X DELETE 'http://127.0.0.1:51202/experts/user/pm?user_id=xinyuan'
```

#### 2. 
```bash
#  OASIS  #oasis#  session
curl 'http://127.0.0.1:51202/sessions/oasis?user_id=xinyuan'
```

#### 3. Workflow 
```bash
#  workflows
curl 'http://127.0.0.1:51202/workflows?user_id=xinyuan'

#  workflow layout
curl -X POST 'http://127.0.0.1:51202/workflows' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","name":"trio_discussion","schedule_yaml":"version:1\nplan:\n - expert: \"creative#temp#1\"","description":"","save_layout":true}'
```

#### 4. Layout 
```bash
#  YAML  layout
curl -X POST 'http://127.0.0.1:51202/layouts/from-yaml' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","yaml_source":"version:1\nplan:\n - expert: \"creative#temp#1\"","layout_name":"trio_layout"}'
```

#### 5. /
```bash
# 
curl -X POST 'http://127.0.0.1:51202/topics' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","question":"","max_rounds":3,"schedule_yaml":"version:1\nplan:\n - expert: \"creative#temp#1\"","discussion":true}'

#  topic_id
curl -X POST 'http://127.0.0.1:51202/topics' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"xinyuan","question":"","max_rounds":3,"schedule_yaml":"version:1\nplan:\n - expert: \"creative#temp#1\"","discussion":true,"callback_url":"http://127.0.0.1:51200/system_trigger","callback_session_id":"my-session"}'

# 
curl 'http://127.0.0.1:51202/topics/{topic_id}?user_id=xinyuan'

# 
curl 'http://127.0.0.1:51202/topics/{topic_id}/conclusion?user_id=xinyuan&timeout=300'

# 
curl -X DELETE 'http://127.0.0.1:51202/topics/{topic_id}?user_id=xinyuan'

# 
curl 'http://127.0.0.1:51202/topics?user_id=xinyuan'
```

#### 6. 
```bash
# SSE 
curl 'http://127.0.0.1:51202/topics/{topic_id}/stream?user_id=xinyuan'
```

****
- Workflows (YAML): `data/user_files/{user}/oasis/yaml/{file}.yaml` YAML  layout JSON
- : `data/oasis_user_experts/{user}.json`
- : `data/oasis_topics/{user}/{topic_id}.json`

****  MCP  `list_oasis_experts``add_oasis_expert``update_oasis_expert``delete_oasis_expert``list_oasis_sessions``set_oasis_workflow``list_oasis_workflows``yaml_to_layout``post_to_oasis``check_oasis_discussion``cancel_oasis_discussion``list_oasis_topics` 

## 



```bash
bash selfskill/scripts/run.sh configure --init
bash selfskill/scripts/run.sh configure --batch \
  LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx4c74 \
  LLM_BASE_URL=https://deepseek.com \
  LLM_MODEL=deepseek-chat \
  LLM_VISION_SUPPORT=true \
  TTS_MODEL=gemini-2.5-flash-preview-tts \
  TTS_VOICE=charon \
  PORT_AGENT=51200 \
  PORT_SCHEDULER=51201 \
  PORT_OASIS=51202 \
  PORT_FRONTEND=51209 \
  PORT_BARK=58010 \
  OPENCLAW_API_URL=http://127.0.0.1:18789/v1/chat/completions \
  OPENAI_STANDARD_MODE=false
bash selfskill/scripts/run.sh add-user system <your-password>
```

 `configure --show` 

```
  PORT_SCHEDULER=51201
  PORT_AGENT=51200
  PORT_FRONTEND=51209
  PORT_OASIS=51202
  OASIS_BASE_URL=http://127.0.0.1:51202
  PORT_BARK=58010
  INTERNAL_TOKEN=f1aa****57e7          # 
  LLM_API_KEY=sk-7****4c74
  LLM_BASE_URL=https://deepseek.com
  LLM_MODEL=deepseek-chat
  LLM_VISION_SUPPORT=true
  TTS_MODEL=gemini-2.5-flash-preview-tts
  TTS_VOICE=charon
  OPENAI_STANDARD_MODE=false
```

> `INTERNAL_TOKEN` `PUBLIC_DOMAIN` / `BARK_PUBLIC_URL`  tunnel 

## 

```bash
cd /home/avalon/TeamClaw

# 
bash selfskill/scripts/run.sh setup
bash selfskill/scripts/run.sh configure --init
bash selfskill/scripts/run.sh configure --batch LLM_API_KEY=sk-xxx LLM_BASE_URL=https://api.deepseek.com LLM_MODEL=deepseek-chat
bash selfskill/scripts/run.sh add-user system MyPass123

# 
bash selfskill/scripts/run.sh start

#  API
curl -X POST http://127.0.0.1:51200/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer system:MyPass123" \
  -d '{"model":"mini-timebot","messages":[{"role":"user","content":""}],"stream":false,"session_id":"default"}'

# 
bash selfskill/scripts/run.sh stop
```

## 

-  skill  `selfskill/scripts/`
-  PID `start` 
- `INTERNAL_TOKEN` 
- : `logs/launcher.log`

- 
- openclaw session fileskillopenclaw agentopenclaw

---

## ⚠️ Before First Launch — Required Configuration

Before starting TeamClaw for the first time, the following environment variables **must** be configured. Without them the service will not function correctly.

### 1. LLM Configuration (Required)

> ⚠️ **LLM API ≠ OpenClaw API — They are two completely separate sets of credentials!**
>
> - `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL` → Your **LLM provider** (DeepSeek, OpenAI, Google, etc.). Used for the built-in Agent's conversations and OASIS experts.
> - `OPENCLAW_API_URL` / `OPENCLAW_API_KEY` → Your **local OpenClaw service** endpoint. Used only for orchestrating OpenClaw agents on the visual Canvas.
>
> Do **NOT** mix them up. They point to different services, use different keys, and serve different purposes.

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_API_KEY` | Your LLM provider's API key. **This is mandatory.** | `sk-xxxxxxxxxxxxxxxx` |
| `LLM_BASE_URL` | Base URL of your LLM provider's API endpoint. | `https://api.deepseek.com` |
| `LLM_MODEL` | The model name to use for conversations. | `deepseek-chat` / `gpt-4o` / `gemini-2.5-flash` |

```bash
bash selfskill/scripts/run.sh configure --batch \
  LLM_API_KEY=sk-your-key \
  LLM_BASE_URL=https://api.deepseek.com \
  LLM_MODEL=deepseek-chat
```

### 2. OpenClaw Integration (Required for visual workflow orchestration)

> ⚠️ **Reminder: OpenClaw API is NOT the same as LLM API above!**
>
> The `OPENCLAW_*` variables below point to your **locally running OpenClaw service**, not to an external LLM provider. They have completely different URLs, keys, and purposes.

These variables are **required** if you intend to use the OASIS visual Canvas to orchestrate OpenClaw agents:

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENCLAW_SESSIONS_FILE` | Absolute path to the OpenClaw `sessions.json` file. Used to discover existing OpenClaw agent sessions and make them available for drag-and-drop orchestration on the visual Canvas. **The frontend orchestration panel will NOT load OpenClaw sessions if this is not set.** | `/projects/.moltbot/agents/main/sessions/sessions.json` |
| `OPENCLAW_API_URL` | The OpenClaw backend API endpoint. This changes with the gateway port. **You MUST first enable OpenClaw's OpenAI-compatible API interface** before configuring this. Include the full path with `/v1/chat/completions`. | `http://127.0.0.1:18789/v1/chat/completions` |
| `OPENCLAW_API_KEY` | The API key for accessing OpenClaw via its OpenAI-compatible endpoint. Required if your OpenClaw instance has authentication enabled. | `your-openclaw-key` |

> **Important**: `OPENCLAW_API_URL` changes whenever the OpenClaw gateway port changes. Always verify the port is correct and that the OpenClaw OpenAI-compatible interface is enabled before starting TeamClaw.

```bash
bash selfskill/scripts/run.sh configure --batch \
  OPENCLAW_SESSIONS_FILE=/projects/.moltbot/agents/main/sessions/sessions.json \
  OPENCLAW_API_URL=http://127.0.0.1:18789/v1/chat/completions \
  OPENCLAW_API_KEY=your-openclaw-key-if-needed
```

### 3. Cloudflare Tunnel (Optional — for remote access)

To expose the Web UI to the public internet for remote visual workflow programming (e.g., from a mobile phone):

- The `tunnel.py` script will automatically write `PUBLIC_DOMAIN` and `BARK_PUBLIC_URL` into `.env` when a Cloudflare Tunnel is established.
- No manual configuration is needed — just run the tunnel script and the frontend becomes accessible via HTTPS on the public domain.
- **Non-blocking start**: `tunnel.py` blocks the terminal by default (main thread joins tunnel threads). To start it without blocking the agent or terminal, run it in the background:

```bash
nohup python scripts/tunnel.py > logs/tunnel.log 2>&1 &
sleep 30  # Wait for tunnels to be established and PUBLIC_DOMAIN written to .env
```

---

## ⚠️ 首次启动前 — 必须配置项

首次启动 TeamClaw 之前，以下环境变量**必须**配置完毕，否则服务无法正常运行。

### 1. LLM 配置（必填）

> ⚠️ **LLM API ≠ OpenClaw API —— 这是两组完全不同的配置！**
>
> - `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL` → 你的 **LLM 服务商**（DeepSeek、OpenAI、Google 等）。用于内置 Agent 对话和 OASIS 专家调用。
> - `OPENCLAW_API_URL` / `OPENCLAW_API_KEY` → 你的 **本地 OpenClaw 服务** 端点。仅用于在可视化画布上编排 OpenClaw Agent。
>
> **切勿混淆！** 它们指向不同的服务，使用不同的密钥，用途完全不同。

| 变量 | 说明 | 示例 |
|------|------|------|
| `LLM_API_KEY` | LLM 服务商的 API 密钥，**必填项**。 | `sk-xxxxxxxxxxxxxxxx` |
| `LLM_BASE_URL` | LLM 服务商的 API 基础地址。 | `https://api.deepseek.com` |
| `LLM_MODEL` | 使用的模型名称。 | `deepseek-chat` / `gpt-4o` / `gemini-2.5-flash` |

```bash
bash selfskill/scripts/run.sh configure --batch \
  LLM_API_KEY=sk-your-key \
  LLM_BASE_URL=https://api.deepseek.com \
  LLM_MODEL=deepseek-chat
```

### 2. OpenClaw 集成配置（使用可视化编排时必填）

> ⚠️ **再次提醒：OpenClaw API 和上面的 LLM API 不是同一个东西！**
>
> 下面的 `OPENCLAW_*` 变量指向你 **本地运行的 OpenClaw 服务**，而非外部 LLM 服务商。它们的 URL、密钥和用途完全不同。

如果你需要使用 OASIS 可视化画布来编排 OpenClaw Agent，以下变量**必须配置**：

| 变量 | 说明 | 示例 |
|------|------|------|
| `OPENCLAW_SESSIONS_FILE` | OpenClaw `sessions.json` 文件的绝对路径。用于获取已有的 OpenClaw Agent session 号，使其可以在可视化画布中被拖拽使用。**未配置此项时前端编排面板将无法加载 OpenClaw sessions。** | `/projects/.moltbot/agents/main/sessions/sessions.json` |
| `OPENCLAW_API_URL` | OpenClaw 后端 API 地址。该地址随 gateway 端口变化而变化。**必须先开启 OpenClaw 的 OpenAI 兼容接口**，填写包含 `/v1/chat/completions` 的完整路径。 | `http://127.0.0.1:18789/v1/chat/completions` |
| `OPENCLAW_API_KEY` | 通过 OpenAI 兼容接口访问 OpenClaw 时使用的 API Key。如果你的 OpenClaw 实例启用了鉴权，则此项必填。 | `your-openclaw-key` |

> **重要提醒**：`OPENCLAW_API_URL` 会随着 OpenClaw gateway 端口的改变而改变，启动前请务必确认端口正确，且 OpenClaw 的 OpenAI 兼容接口已开启。

```bash
bash selfskill/scripts/run.sh configure --batch \
  OPENCLAW_SESSIONS_FILE=/projects/.moltbot/agents/main/sessions/sessions.json \
  OPENCLAW_API_URL=http://127.0.0.1:18789/v1/chat/completions \
  OPENCLAW_API_KEY=your-openclaw-key-if-needed
```

### 3. Cloudflare Tunnel（可选 — 用于远程访问）

如需将前端 Web UI 通过公网 HTTPS 安全暴露，以便在手机或其他远程设备上进行可视化多 Agent 工作流编排：

- 运行 `tunnel.py` 脚本后，Cloudflare Tunnel 会自动建立，并将 `PUBLIC_DOMAIN` 和 `BARK_PUBLIC_URL` 写入 `.env`。
- 无需手动配置，启动隧道后即可通过 HTTPS 公网域名访问前端。
- **非阻塞启动**：`tunnel.py` 默认会阻塞终端（主线程 join 等待隧道线程）。如需避免阻塞 Agent 或终端，请后台启动：

```bash
nohup python scripts/tunnel.py > logs/tunnel.log 2>&1 &
sleep 30  # 等待隧道建立完成，PUBLIC_DOMAIN 写入 .env
```
