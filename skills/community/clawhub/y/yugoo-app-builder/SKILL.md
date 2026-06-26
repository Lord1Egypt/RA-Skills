---
name: yugoo-app-builder
description: Build full-stack web applications using 语构's chat-driven development platform. Manages conversations, sends development instructions, monitors build progress, extracts results (generated files, summaries, task status), publishes applications, and manages versions.
metadata:
  slug: yugoo-app-builder
  display_name: 语构 App Builder
  homepage: https://creo4u.com
  env:
    - name: CREO4U_SKILL_API_KEY
      required: true
      description: API key for authenticating with the 语构 (Yugoo) platform. Use a least-privilege or revocable key.
  dependencies:
    - requests
---

# Installation

## Prerequisites

Before using this skill, ensure you have the `CREO4U_SKILL_API_KEY` environment variable set.

### Setup API Key

**Option 1: Provide API Key during installation**
```bash
export CREO4U_SKILL_API_KEY="your_api_key_here"
```

**Option 2: If not provided, the skill will prompt for it**
- If `CREO4U_SKILL_API_KEY` is already set in your environment, the skill will use it directly
- If not set, the skill will ask you to provide the API key

### After Installation

Once installed, all CLI commands will automatically use the `CREO4U_SKILL_API_KEY` environment variable — no need to pass `--token` or any API key parameter.

---

# 语构 App Builder

语构 is a **chat-driven full-stack application builder**. Users describe what they want in natural language and 语构 generates a **production-ready web application**, including frontend UI, backend services, database schema, and a live development environment.

This skill enables AI agents to interact with the **语构 platform** to create, iterate, publish, and deploy applications.

All platform operations must be executed through the CLI script:

```bash
python scripts/yugoo_cli.py [global options] <command> [command options]
```

**IMPORTANT: Argument Order** — Global options (`--token`, `--base-url`, `--insecure`, `--timeout`) must appear **BEFORE** the subcommand. Placing them after the subcommand will cause a parse error.

```bash
# ✅ Correct — global options before subcommand
python scripts/yugoo_cli.py --token TOKEN create --name "My App"

# ❌ Wrong — global options after subcommand
python scripts/yugoo_cli.py create --token TOKEN --name "My App"
```

> **Note**: The `--insecure` flag disables TLS certificate verification. Only use it in controlled test environments — never for production or when transmitting real API keys.

Do **not** call platform APIs directly. Always use the CLI commands provided by this skill.

---

# When to Use This Skill

Use this skill whenever the user wants to:

* create a **website** or **web application**
* build a **dashboard** or **admin panel**
* create a **SaaS product** or **internal tool**
* build a **full-stack application** with frontend + backend
* build a **landing page**
* create a **browser game** or **mini game**
* iterate on an existing **语构 project**
* publish or deploy an **语构 application**
* check sandbox health or preview URLs
* manage application **versions**
* **copy** an existing application (own or from market)
* **clone** an app from the **app market**
* **switch** between application versions
* **delete** or **finalize** a version

Do **not** use this skill for unrelated programming tasks.

---

# Routing Keywords

Trigger this skill if the request includes concepts such as:

* build a website
* create a webpage
* build a web app
* create a SaaS
* build a dashboard
* create an admin panel
* build an internal tool
* create a landing page
* build a browser game
* create a mini game
* generate a web product
* make a snake game webpage
* build a todo web app
* create a blog site
* publish this app
* deploy this application
* copy this app
* clone an app from market
* browse app market
* switch to version
* list versions
* delete version
* finalize version

---

# Example Requests

Examples that should route to this skill:

* "Create a todo list web app"
* "Build a personal blog website"
* "Make a dashboard for sales analytics"
* "Create a SaaS landing page"
* "Build an admin panel"
* "Write a snake game webpage"
* "Create a browser game"
* "Build a mini web game"
* "Modify my 语构 project"
* "Publish this 语构 app"
* "Deploy my application"

---

# Application Development Description Guidelines

## ✅ DO: Simple, Focused Requests

### For New Applications
Describe the **core functionality** in 1-2 sentences:

```
"Build a todo app where users can add tasks, mark them complete, and delete them"
"Create a dashboard to display sales data with charts and filters"
"Build a landing page for a SaaS product with pricing section and contact form"
```

### For Bug Fixes or Optimizations (1-2 changes per request)

**✅ Correct - Single Focus:**
```
"Fix the submit button not responding on the contact form"
"Optimize the loading speed of the data table"
"Add error handling for invalid email input"
"Fix the date picker not showing correct format"
```

**✅ Correct - Two Related Changes:**
```
"Fix the login button styling and add a loading indicator"
"Optimize the database query and add caching for faster response"
"Fix the mobile layout and adjust the navigation menu"
```

**❌ WRONG - Too Complex (DO NOT use):**
```
"Fix the login button, optimize the database, add user authentication, redesign the homepage, and deploy to production"
```

## ⚠️ IMPORTANT: Complexity Limits

When sending messages to the `chat` API:

| Request Type | Max Items |
|--------------|-----------|
| Bug fixes | 1-2 related bugs |
| Feature additions | 1-2 related features |
| Optimizations | 1-2 related optimizations |
| UI changes | 1-2 related components |

**Rationale**: 语构 platform works best with focused, incremental changes. Complex multi-part requests may result in incomplete implementation or unexpected behavior.

## Iterative Development Pattern

For complex requirements, break them into multiple chat messages:

```bash
# Round 1: Build basic structure
chat -c $CID -m "Build a todo app with add and list features" --watch

# Round 2: Add one feature
chat -c $CID -m "Add delete functionality to todo items" --watch

# Round 3: Add another feature
chat -c $CID -m "Add edit functionality and local storage" --watch

# Round 4: Polish
chat -c $CID -m "Improve the UI styling and add animations" --watch
```

---

# How to Describe Application Requirements

## ✅ Do: Keep It Simple

Describe **what the application should do** in one or two sentences:

```
"Build a todo app where users can add tasks, mark them complete, and delete them"
"Create a dashboard to display sales data with charts and filters"
```

## ❌ Don't: Over-Specify

Avoid:
- Technology stack (e.g., "use React", "use FastAPI")
- Performance requirements (e.g., "handle 1000 concurrent users")
- Architecture constraints (e.g., "use microservices")
- Detailed feature lists

**For iterative modifications, keep requests brief — only describe the change needed, not the full application again.**

**For bug fixes or optimizations, limit to 1-2 related changes per request.** See [Application Development Description Guidelines](#application-development-description-guidelines) for details.

The platform handles technical decisions automatically.

---

# Model Selection

The `chat` command accepts an optional `--model-choice` parameter that selects which model the **Task agent** uses for this message. The Pilot agent always uses the platform default and is **not** affected by this flag.

## Accepted values

| Value | Meaning |
|-------|---------|
| *(omitted)* or `auto` | Smart routing — platform picks the best model |
| `economy` | Preset: cheaper / faster models |
| `advance` | Preset: balanced cost vs. capability |
| `expert` | Preset: highest-capability models |
| `<model-id>` | A concrete model id from `python scripts/yugoo_cli.py models` (e.g. `claude-sonnet-4-6`) |

Format constraint: `^[A-Za-z0-9._\-]+$`, max length 80.

## Typical usage

```bash
# Discover available choices
python scripts/yugoo_cli.py models

# Pick a preset
python scripts/yugoo_cli.py chat -c $CID -m "Build a SaaS landing page" --model-choice expert --watch

# Pin a concrete model id
python scripts/yugoo_cli.py chat -c $CID -m "Add e2e tests" --model-choice claude-sonnet-4-6 --watch
```

## When to set it explicitly

- The user asks for a specific model ("use Sonnet", "switch to the cheaper model").
- You're running a high-stakes / complex change and want the `expert` preset.
- You're doing many trivial iterations and want the `economy` preset to save credits.

For most cases, leave it unset (smart routing).

---

# Stateless Execution Model

The CLI script is **stateless**. It does not store workflow state between calls.

Application workflow state is maintained by the 语构 platform and must be tracked via:

* `conversation_id` — the unique session identifier
* `message_id` — identifies a specific message/generation run

Agents must pass the appropriate identifiers when continuing conversations or checking results.

---

# Application Lifecycle

语构 applications follow a standard lifecycle:

## 1. Initial Creation

For a new application:

1. Start with a `chat` request describing the product
2. The platform generates the application automatically
3. Application is available in the development environment

## 2. Multi-Round Modification

After an application has been created:

* Continue using `chat` with the same `conversation_id`
* Chat messages modify the existing application
* No additional generation step required

## 3. Publishing

Publishing deploys the application to production:

* Use `publish` command to trigger deployment
* Use `publish --wait` to auto-poll until deployment completes
* After successful publish, the app is live at the preview URL

---

# Application URLs

语构 provides URLs during the lifecycle:

## Development/Preview URL

After the application is created, access it at:

```
https://preview-{conversation_id}.creo4u.com/
```

This URL is for:
* viewing the application
* testing features
* development iteration

## Production URL

After publishing succeeds, the application is accessible at:

```
https://preview-{conversation_id}.creo4u.com/
```

This is the **public production URL** of the deployed application.

Share this URL only after publishing completes successfully.

---

# Standard Workflow

## Create New Application

```
create → chat --watch → publish --wait → urls
```

## Iterate on Existing Application

```
chat --watch → result → chat --watch → result → ...
```

## Publish Application

```
publish --wait → urls
```

## Take Down Application

```
unpublish
```

## Copy Own Application

```
copy → chat --watch → result → publish --wait
```

## Clone from App Market

```
market-list → clone-market → chat --watch → result → publish --wait
```

## Version Management

```
versions → restore-version → chat --watch → finalize-version
```

## Build with Attachments

```
upload --file → chat --attachment OSS_PATH --watch → publish --wait → urls
```

## Build from Local File

```
chat --file /path/to/requirements.txt --watch → result → publish --wait → urls
```

---

# Complete Workflow Example

```bash
# Step 1: Create a conversation
CONV=$(python scripts/yugoo_cli.py create --name "Todo App")
CID=$(echo $CONV | python -c "import sys,json; print(json.load(sys.stdin)['conversation_id'])")

# Step 2: Send development instructions and watch progress
# The poll_completed snapshot contains cost/time in assistant messages
python scripts/yugoo_cli.py chat \
  -c $CID \
  -m "Build a todo app with add, complete, and delete features" \
  --watch

# Step 3: Publish the application (auto-wait for completion)
python scripts/yugoo_cli.py publish -c $CID --wait

# Step 4: Get the production URL
python scripts/yugoo_cli.py urls -c $CID
```

---

# Available Commands

**Note**: All commands automatically use the `CREO4U_SKILL_API_KEY` environment variable for authentication.

## create

Create a new conversation.

```bash
python scripts/yugoo_cli.py create [--name NAME]
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--name` | `New Conversation` | Conversation name |

**Output**: JSON with `conversation_id`, `name`, `status`, `created_at`.

---

## upload

Upload a local file as a chat attachment. The file is uploaded to OSS and the returned `oss_path` can be passed to `chat --attachment`.

```bash
python scripts/yugoo_cli.py upload --file /path/to/file
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--file` | Yes | Local file path to upload (max 50MB) |

**Output**: JSON with `oss_path`, `filename`, `file_md5`, `size_bytes`.

```json
{"oss_path": "chat/attachments/123/abc123def456/document.pdf", "filename": "document.pdf", "file_md5": "abc123def456...", "size_bytes": 1048576}
```

**Example — Upload then chat with attachment:**
```bash
# Step 1: Upload the file
UPLOAD=$(python scripts/yugoo_cli.py upload --file design.png)
OSS_PATH=$(echo $UPLOAD | python -c "import sys,json; print(json.load(sys.stdin)['oss_path'])")

# Step 2: Send message with attachment
python scripts/yugoo_cli.py chat -c $CID -m "参考这个设计图来实现页面" --attachment "$OSS_PATH" --watch
```

---

## chat

Send a message and optionally watch for completion via polling. This is the primary workflow command.

```bash
python scripts/yugoo_cli.py chat -c CID -m "message" [--watch] [--attachment OSS_PATH]
python scripts/yugoo_cli.py chat -c CID -f /path/to/file [--watch]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | No | Conversation ID (omit to auto-create) |
| `-m`, `--content` | No* | Message content (use `-` to read from stdin) |
| `-f`, `--file` | No* | Read message content from a local file path |
| `-w`, `--watch` | No | Poll for completion after sending message (15s interval) |
| `--agent-name` | No | Specific agent to handle the message |
| `--context` | No | JSON string for additional context |
| `--attachment` | No | OSS path of uploaded attachment (repeatable for multiple files) |
| `--model-choice` | No | Model selection for the Task agent. Accepts a preset (`auto` \| `economy` \| `advance` \| `expert`) or a concrete model id from the `models` command. Omit (or pass `auto`) to use smart routing. Only affects the Task agent; the Pilot agent always uses the platform default. |

*Either `--content` or `--file` is required. `--file` takes priority if both are provided.

**Output without `--watch`**: Single JSON line with `message_id`, `conversation_id`.

**Output with `--watch`**: Polling mode with completion status
```json
{"event": "message_accepted", "message_id": "...", "conversation_id": "..."}
{"event": "poll", "iteration": 1, "state": "pending"}
{"event": "poll", "iteration": 2, "state": "running"}
{"event": "poll_completed", "iteration": 3, "state": "completed", "snapshot": {...}}
```

**Important**:
- Use `--watch` for most cases — it sends the message AND polls for completion in one command.
- Use `--file` to send a local file's content as the message — useful for long requirement documents or pre-written prompts.
- Use `--content -` to read long prompts from stdin.
- Use `upload` command first to get `oss_path`, then pass it via `--attachment`.
- Use `--model-choice` to override the default model routing (see [Model Selection](#model-selection)).

**Example — pick a model preset:**

```bash
# Use the high-capability "expert" preset for the Task agent
python scripts/yugoo_cli.py chat -c $CID -m "Refactor the auth flow" --model-choice expert --watch

# Use a concrete model id (look it up via the `models` command first)
python scripts/yugoo_cli.py chat -c $CID -m "Add tests" --model-choice claude-sonnet-4-6 --watch
```

---

## models

List available model presets and concrete model ids for use with `chat --model-choice`. This is a public endpoint and does not consume credit.

```bash
python scripts/yugoo_cli.py models
```

**Output**:
```json
{
  "presets": [
    {"id": "auto", "display_name": "Auto", "description": "Smart routing", "is_default": true, "first_model": "...", "fallback_chain": ["..."]},
    {"id": "economy", "display_name": "Economy", "description": "Cheaper, faster models", "first_model": "...", "fallback_chain": ["..."]},
    {"id": "advance", "display_name": "Advance", "description": "Balanced", "first_model": "...", "fallback_chain": ["..."]},
    {"id": "expert", "display_name": "Expert", "description": "Highest capability", "first_model": "...", "fallback_chain": ["..."]}
  ],
  "models": [
    {"id": "claude-sonnet-4-6", "display_name": "Claude Sonnet 4.6", "series": "claude", "price_tier": "advance", "is_latest": true, "enabled": true, "context_window": 200000}
  ],
  "default_choice": "auto"
}
```

**When to use**:
- Before the first chat in a session, if you want a non-default model.
- When the user explicitly asks "which models can I use?" / "switch to a cheaper model" / etc.
- Pass either a preset `id` (e.g. `expert`) or a concrete model `id` (e.g. `claude-sonnet-4-6`) to `chat --model-choice`.

---

## publish

Trigger deployment to production.

```bash
python scripts/yugoo_cli.py publish -c CID [--wait]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Conversation ID to publish |
| `-w`, `--wait` | No | Auto-poll publish status until published or failed |

**Examples:**

**1. Publish and manually check status:**

```bash
python scripts/yugoo_cli.py publish -c $CID
```

**2. Publish and auto-wait for completion (recommended):**

```bash
python scripts/yugoo_cli.py publish -c $CID --wait
```

**Important:**
- Application must be created before publishing
- After successful publish, the app is live at the preview URL
- Use `--wait` flag to avoid manual polling

---

## publish-status

Check the status of a deployment.

```bash
python scripts/yugoo_cli.py publish-status -c CID
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Conversation ID |

**Output**: JSON with `status`: `created`, `publishing`, `published`, or `failed`

**Usage Pattern:**

```bash
# Publish and auto-wait for completion (recommended)
python scripts/yugoo_cli.py publish -c $CID --wait

# Or check status manually
python scripts/yugoo_cli.py publish-status -c $CID
```

**Tip:** Use `publish --wait` to avoid manual polling.

---

## unpublish

Take down a deployed application (removes the public production URL).

```bash
python scripts/yugoo_cli.py unpublish -c CID
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Conversation ID to unpublish |

**Example:**

```bash
python scripts/yugoo_cli.py unpublish -c $CID
```

**Important:**
- Application must have been published before it can be unpublished
- After unpublishing, the production URL is no longer accessible
- The conversation and source files are preserved; only the deployment is removed
- You can `publish` the application again later to restore the deployment

---

## messages

Get the full conversation snapshot (all messages and state).

```bash
python scripts/yugoo_cli.py messages -c CID
```

**Output**: Complete snapshot JSON with all runs, messages, panels, and metadata.

---

## result

Extract structured development results from the conversation snapshot. This is the recommended way to get results after a `chat --watch` completes.

```bash
python scripts/yugoo_cli.py result -c CID [--message-id MID]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Conversation ID |
| `--message-id` | No | Specific message run (default: latest) |

**Output**:
```json
{
  "conversation_id": "...",
  "message_id": "...",
  "status": "completed",
  "summary": "Built a full-stack todo application...",
  "files_generated": ["src/App.tsx", "backend/main.py"],
  "files_modified": ["package.json"],
  "assistant_messages": ["..."],
  "tasks": [
    {"task_id": "...", "title": "Generate frontend code", "status": "completed", "type": "streaming_multi_file"}
  ],
  "error": null,
  "token_usage": {"prompt_tokens": 1234, "completion_tokens": 5678, "total_tokens": 6912},
  "credit_usage": 100,
  "started_at": 1705771805000,
  "completed_at": 1705771900000
}
```

---

## stop

Stop message generation in progress.

```bash
python scripts/yugoo_cli.py stop -c CID --message-id MID
```

---

## start-runtime

Start or restart the conversation runtime (container environment).

```bash
python scripts/yugoo_cli.py start-runtime -c CID
```

Use this after a container has been reclaimed due to inactivity.

---

## list

List conversations with pagination and filtering.

```bash
python scripts/yugoo_cli.py list [--limit N] [--offset N] [--keyword KW] [--sort-by FIELD] [--sort-order asc|desc]
```

---

## get

Get conversation details.

```bash
python scripts/yugoo_cli.py get -c CID
```

---

## delete

Terminate a conversation.

```bash
python scripts/yugoo_cli.py delete -c CID
```

---

## health

Check sandbox services health (frontend, backend, sandbox interface).

```bash
python scripts/yugoo_cli.py health -c CID
```

**Output**:
```json
{
  "frontend": {"ready": true, "status_code": 200, "message": "Frontend service is ready"},
  "backend": {"ready": true, "status_code": 200, "message": "Backend service is ready"},
  "sandbox": {"ready": true, "status_code": 200, "message": "Sandbox service is ready"},
  "all_ready": true
}
```

---

## urls

Get sandbox, preview, and backend URLs for the development environment.

```bash
python scripts/yugoo_cli.py urls -c CID
```

**Output**:
```json
{"sandbox_url": "https://sandbox-xxx.domain.com", "preview_url": "https://preview-xxx.domain.com", "backend_url": "https://backend-xxx.domain.com"}
```

---

## download

Download workspace as a zip file.

```bash
python scripts/yugoo_cli.py download -c CID
```

**Output**: JSON with `download_url`, `filename`, `size_mb`, `md5`.

---

## versions

List all saved versions for a conversation.

```bash
python scripts/yugoo_cli.py versions -c CID [--sort-order asc|desc]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Conversation ID |
| `--sort-order` | No | Sort direction: `asc` (oldest first) or `desc` (newest first, default) |

**Output**: JSON with `conversation_id`, `current_version`, `versions` array (each with `version`, `timestamp`, `is_wip`, `is_published`, `description`, `from_version`), and `total` count.

**Example**:
```bash
python scripts/yugoo_cli.py versions -c $CID
# Output: {"conversation_id": "...", "current_version": 3, "versions": [...], "total": 3}
```

---

## current-version

Get the current active version number and its metadata.

```bash
python scripts/yugoo_cli.py current-version -c CID
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Conversation ID |

**Output**: JSON with `conversation_id`, `current_version`, `is_wip`, `from_version`, `description`.

---

## restore-version

Switch workspace to a specific version. This changes the active codebase and restarts the sandbox.

```bash
python scripts/yugoo_cli.py restore-version -c CID --version N
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Conversation ID |
| `--version` | Yes | Version number to switch to |

**Output**: JSON with `success`, `version`, `mode` (`tag` or `wip`), `message`.

**Important**:
- Switching versions restarts the sandbox runtime automatically.
- Cannot switch versions while another operation is in progress (returns 409).
- After switching, use `chat` to continue development from that version.

---

## copy

Create a deep copy of an existing conversation (own application).

```bash
python scripts/yugoo_cli.py copy -c CID [--new-name NAME] [--wait]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Source conversation ID |
| `--new-name` | No | Name for the copy (default: "{original name}（副本）") |
| `-w`, `--wait` | No | Auto-poll copy status until workspace is ready (5s interval, max 10 minutes) |

**Output**: JSON with `conversation_id`, `name`, `status`, `created_at` of the new conversation.

**Important**:
- Creates a completely independent copy with new conversation ID
- Workspace files are copied in the background (1-30 seconds)
- The new conversation is immediately usable for chat commands
- Use `--wait` to block until workspace files are fully copied

**Example**:
```bash
# Copy an existing app (without waiting)
NEW=$(python scripts/yugoo_cli.py copy -c $CID --new-name "My App V2")
NEW_CID=$(echo $NEW | python -c "import sys,json; print(json.load(sys.stdin)['conversation_id'])")

# Copy and wait for workspace to be ready
NEW=$(python scripts/yugoo_cli.py copy -c $CID --new-name "My App V2" --wait)
NEW_CID=$(echo $NEW | python -c "import sys,json; print(json.load(sys.stdin)['conversation_id'])")

# Iterate on the copy
python scripts/yugoo_cli.py chat -c $NEW_CID -m "Add dark mode support" --watch
```

---

## market-list

Browse and search the app market.

```bash
python scripts/yugoo_cli.py market-list [--limit N] [--offset N] [--keyword KW] [--category-id ID] [--sort-by FIELD]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--limit` | No | Max results (default: 20) |
| `--offset` | No | Pagination offset (default: 0) |
| `--keyword` | No | Search keyword |
| `--category-id` | No | Filter by category ID |
| `--sort-by` | No | Sort field (e.g. `view_count`, `clone_count`, `created_at`) |

**Output**: JSON with `items` array containing market item details (item_id, title, description, clone_count, view_count, etc.) and pagination info.

**Example**:
```bash
# Search for todo apps
python scripts/yugoo_cli.py market-list --keyword "todo"

# Browse most popular apps
python scripts/yugoo_cli.py market-list --sort-by view_count --limit 10
```

---

## clone-market

Clone an app from the app market into your conversation list.

```bash
python scripts/yugoo_cli.py clone-market --item-id ITEM_ID
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--item-id` | Yes | Market item ID to clone |

**Output**: JSON with `conversation_id`, `cloned_code`, `cloned_prd`, `cloned_history`, `message_count`.

**Important**:
- The cloned app is created as a new conversation you own
- What gets cloned depends on the original app's clone permission settings:
  - CODE: workspace source files
  - PRD: design documents
  - HISTORY: conversation messages
- Workspace files are copied in the background

**Example - Clone from Market and Iterate**:
```bash
# Step 1: Browse market
python scripts/yugoo_cli.py market-list --keyword "dashboard"

# Step 2: Clone the app (use item_id from market-list result)
CLONE=$(python scripts/yugoo_cli.py clone-market --item-id $ITEM_ID)
CID=$(echo $CLONE | python -c "import sys,json; print(json.load(sys.stdin)['conversation_id'])")

# Step 3: Customize the cloned app
python scripts/yugoo_cli.py chat -c $CID -m "Change the color scheme to dark blue" --watch

# Step 4: Publish your customized version
python scripts/yugoo_cli.py publish -c $CID --wait
```

---

## delete-version

Delete a WIP (work-in-progress) version and revert to the previous version.

```bash
python scripts/yugoo_cli.py delete-version -c CID --version N
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Conversation ID |
| `--version` | Yes | Version number to delete |

**Output**: JSON with `success`, `version`, `reverted_to_version`, `message`.

**Important**:
- Only WIP versions can be deleted. Finalized versions cannot be deleted.
- The workspace automatically reverts to the previous version after deletion.
- Cannot delete a version while another operation is in progress (returns 409).

---

## finalize-version

Finalize (lock) the current WIP version, making it a permanent checkpoint.

```bash
python scripts/yugoo_cli.py finalize-version -c CID
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Conversation ID |

**Output**: JSON with `success`, `version`, `from_version`, `message`.

**Important**:
- Only works when the workspace is on a WIP branch.
- After finalization, the version becomes a permanent tag that cannot be deleted.
- Use this to create stable checkpoints before making major changes.

---

## update-version-desc

Update the description of a specific version.

```bash
python scripts/yugoo_cli.py update-version-desc -c CID --version N --description "description text"
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Conversation ID |
| `--version` | Yes | Version number |
| `--description` | Yes | New description text |

**Output**: JSON with `success`, `version`, `description`, `message`.

---

## rename

Rename a conversation.

```bash
python scripts/yugoo_cli.py rename -c CID --name "New Name"
```

---

## spending

Get message-level spending (cost and time) for a conversation. Supports filtering by `message_id` to query a single message's cost and duration.

```bash
python scripts/yugoo_cli.py spending -c CID [--message-id MID] [--limit N] [--offset N]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Conversation ID |
| `--message-id` | No | Filter by specific message ID |
| `--limit` | No | Max results (default: 50) |
| `--offset` | No | Pagination offset (default: 0) |

**Output**:
```json
{
  "session_id": "202501201430-a1b2c3d4",
  "app_name": "My Web App",
  "total_cost": "1500",
  "total": 1,
  "items": [
    {
      "message_id": "msg-001",
      "message_preview": "Build a login page...",
      "total_cost": "300",
      "record_count": 3,
      "first_billing_at": "2025-01-20T14:30:00",
      "last_billing_at": "2025-01-20T14:35:00",
      "started_at": "2025-01-20T14:30:00",
      "finished_at": "2025-01-20T14:35:00",
      "duration_seconds": 300.0
    }
  ],
  "limit": 20,
  "offset": 0
}
```

**Fields**:
- `total_cost`: Total credits consumed for the entire conversation (integer string)
- `items[].total_cost`: Credits consumed per message/development round
- `items[].started_at` / `finished_at`: Start and end timestamps of the development round
- `items[].duration_seconds`: Duration of the development round in seconds
- `items[].first_billing_at` / `last_billing_at`: Time range of billing for each round

---

# Output Conventions

- **stdout**: JSON lines (one JSON object per line). Machine-readable.
- **stderr**: Error messages and metadata.
- **Exit code 0**: Success.
- **Exit code 1**: Error (details on stderr as JSON).

Every stdout line is a complete, self-contained JSON object. This enables piping to `jq` for filtering and line-by-line processing by AI agents.

---

# Polling Mode

The `chat` and `publish` commands with `--watch` use polling to monitor progress:

- **Interval**: Fixed 15 seconds between polls
- **Single request timeout**: 10 minutes (40 iterations per request)
- **Maximum total timeout**: 1 hour (up to 6 retries)

Polling stops automatically when the run reaches `completed` or `failed` state.

**Recommendation**: Use `--wait` flag for publish command to auto-poll status.

## poll

Resume polling for a message that is still in progress (after a `poll_timeout`).

```bash
python scripts/yugoo_cli.py poll -c CID --message-id MID
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-c`, `--conversation-id` | Yes | Conversation ID |
| `--message-id` | Yes | Message ID to poll |

**Output**: Same as `chat --watch` — emits `poll` events and ends with `poll_completed` or `poll_timeout`.

## CRITICAL: Polling Completion Rules

**You MUST follow these rules strictly when using `chat --watch`:**

1. **Single request timeout is 10 minutes**: Each `chat --watch` or `poll` command polls for up to **10 minutes**. If the development is not done, the CLI emits a `poll_timeout` event and exits. This is normal — development can take longer than 10 minutes.

2. **On `poll_timeout`, you MUST retry using the `poll` command**: When you receive a `poll_timeout` event, immediately run the `poll` command with the same `conversation_id` and `message_id` to resume monitoring. **Do NOT** treat `poll_timeout` as a failure or stop.

3. **Maximum 6 retries (1 hour total)**: You may retry the `poll` command up to **6 times** (including the initial `chat --watch`). This ensures a maximum total timeout of 1 hour (6 × 10 min). If all 6 attempts time out, then treat it as a genuine timeout and report to the user.

   **Retry flow:**
   ```
   chat --watch (attempt 1, up to 10 min)
     → poll_timeout? → poll (attempt 2, up to 10 min)
       → poll_timeout? → poll (attempt 3, up to 10 min)
         → poll_timeout? → poll (attempt 4, up to 10 min)
           → poll_timeout? → poll (attempt 5, up to 10 min)
             → poll_timeout? → poll (attempt 6, up to 10 min)
               → poll_timeout? → report timeout to user
   ```

   **Example:**
   ```bash
   # Initial request
   python scripts/yugoo_cli.py chat -c $CID -m "Build a complex app" --watch
   # If poll_timeout, resume with poll:
   python scripts/yugoo_cli.py poll -c $CID --message-id $MID
   # Repeat poll up to 5 more times if needed
   ```

4. **Wait for ALL tasks to complete**: The polling only ends with `poll_completed` when **every task and phase** in the development pipeline has finished (status = `completed` or `failed`). Do NOT consider the operation done just because an assistant message appeared or a partial result was returned.

5. **Do NOT stop polling on intermediate messages**: During development, the platform may return intermediate status messages such as:
   - "服务正在启动中，预计还需要几分钟时间。前端服务启动后即可访问！"
   - "正在生成代码..."
   - "正在部署..."
   - Any message indicating services are still starting or building

   These are **progress updates, NOT completion signals**. You MUST continue waiting for the `poll_completed` event. **Never** interpret these messages as the final result.

6. **Only `poll_completed` means truly done**:
   - `poll_completed` → Development finished. Proceed to `result` and `spending`.
   - `poll_timeout` → Not finished yet. Retry with `poll` command (up to 6 total attempts).

---

# Error Handling

All HTTP errors produce JSON on stderr:

```json
{"error": {"error": "CONVERSATION_NOT_FOUND", "message": "Conversation not found"}, "status_code": 404}
```

Common error codes:

| Status | Error | Meaning |
|--------|-------|---------|
| 402 | `INSUFFICIENT_CREDIT` | User has insufficient credit |
| 404 | `CONVERSATION_NOT_FOUND` | Conversation does not exist |
| 409 | `CONVERSATION_IN_PROGRESS` | Another message is being processed |
| 409 | `WIP_VERSION_CONFLICT` | Version conflict during message send |
| 409 | `PUBLISH_IN_PROGRESS` | Another publish is being processed |
| 501 | `NOT_IMPLEMENTED` | Feature not available in current mode |

If the conversation is locked (409), wait a few seconds and retry.

---

# Application Copy & Clone Workflow

## Copy Your Own Application

Use `copy` to create an independent copy of your existing application, then iterate on it:

```bash
# Copy the app
NEW=$(python scripts/yugoo_cli.py copy -c $CID --new-name "Todo App V2")
NEW_CID=$(echo $NEW | python -c "import sys,json; print(json.load(sys.stdin)['conversation_id'])")

# Develop on the copy
python scripts/yugoo_cli.py chat -c $NEW_CID -m "Add user authentication" --watch

# Publish the new version
python scripts/yugoo_cli.py publish -c $NEW_CID --wait
```

## Clone from App Market

Use `market-list` to find apps, then `clone-market` to clone into your workspace:

```bash
# Browse the market
python scripts/yugoo_cli.py market-list --keyword "ecommerce" --limit 5

# Clone an app (use item_id from market-list output)
CLONE=$(python scripts/yugoo_cli.py clone-market --item-id $ITEM_ID)
CID=$(echo $CLONE | python -c "import sys,json; print(json.load(sys.stdin)['conversation_id'])")

# Customize the cloned app
python scripts/yugoo_cli.py chat -c $CID -m "Replace product catalog with my inventory" --watch

# Get results and publish
python scripts/yugoo_cli.py result -c $CID
python scripts/yugoo_cli.py publish -c $CID --wait
python scripts/yugoo_cli.py urls -c $CID
```

---

# Version Management Workflow

Versions allow you to create checkpoints, switch between states, and safely experiment.

## View and Switch Versions

```bash
# List all versions
python scripts/yugoo_cli.py versions -c $CID

# Check current version
python scripts/yugoo_cli.py current-version -c $CID

# Switch to an earlier version
python scripts/yugoo_cli.py restore-version -c $CID --version 2
```

## Create a Checkpoint (Finalize)

After development, finalize the current WIP version to create a permanent checkpoint:

```bash
# Develop features
python scripts/yugoo_cli.py chat -c $CID -m "Add payment integration" --watch

# Lock the version as a stable checkpoint
python scripts/yugoo_cli.py finalize-version -c $CID

# Add a description to the version
python scripts/yugoo_cli.py update-version-desc -c $CID --version 3 --description "Added payment integration with Stripe"
```

## Undo Changes (Delete WIP Version)

If a development round didn't go well, delete the WIP version to revert:

```bash
# Check current version (e.g., version 4, WIP)
python scripts/yugoo_cli.py current-version -c $CID

# Delete the WIP version and revert to previous
python scripts/yugoo_cli.py delete-version -c $CID --version 4

# Now back at version 3 — try again
python scripts/yugoo_cli.py chat -c $CID -m "Add payment integration using a different approach" --watch
```

---

# Error Handling Guidance

Agents should handle the following situations:

* publish requested before application has been created
* missing `conversation_id`
* interrupted polling loop
* failed deployment status
* incorrect or missing parameter values

If workflow state is unclear, inspect the conversation or use `result` command before taking the next action.

**Pro Tips:**
- Always check command `--help` when unsure about parameters
- Use `--wait` flag with `publish` to simplify deployment
- Save `conversation_id` from `create` response
- After creation, use `chat` directly for modifications

---

# Application Sharing Rule (IMPORTANT)

- You must share your application **only using the production preview URL** (after it has been published).

Production preview URL format:

```
https://preview-{conversation_id}.creo4u.com/
```

- If the application has **not been published**, you must publish it before sharing with others.

Example publish command:

```bash
python scripts/yugoo_cli.py publish -c $CID --wait
```

---

# Tips

- Use `--watch` with `chat` for the common case — it sends the message and polls for completion.
- Use `--wait` with `publish` to auto-poll deployment status.
- Use `result` after completion to get a clean summary without parsing poll events.
- Use `--file` with `chat` to send a local file's content as the message, useful for long requirement documents or pre-written prompts.
- The `--content -` flag reads message content from stdin, useful for long prompts.
- `conversation_id` is abbreviated as `-c` in all commands for convenience.
- Always check `result` output for `status: "failed"` and `error` field to detect failures.
- Use `health` to verify the sandbox is ready before sending development instructions.
- Use `start-runtime` to restart a container that was reclaimed due to inactivity.

---

# Development Completion Best Practice

**After an application is built, do NOT manually inspect the generated code files.**

After `chat --watch` (or `poll`) completes with `poll_completed`:

1. Query **Development Cost** and **Development Time** using the `spending` command with `--message-id`:

```bash
python scripts/yugoo_cli.py spending -c "$CID" --message-id "$MID"
```

Extract from the response:
- **Development Cost**: `items[0].total_cost` (Credits)
- **Development Time**: `items[0].duration_seconds` (seconds)

2. Publish and get URLs:

```bash
python scripts/yugoo_cli.py publish -c "$CID" --wait
python scripts/yugoo_cli.py urls -c "$CID"
```

Then respond with the following **fixed format** (do NOT change field names or order):

```
**Application Summary**: [one-line description of what was built and key features]

**Preview URL**: https://preview-{conversation_id}.creo4u.com/

**Publish URL**: [url field from publish command output]

**Publish Status**: [published / failed]

**Development Cost**: [N] Credits

**Development Time**: [N]s
```

**IMPORTANT**: Always publish after development completes. Never skip any field. Always include both Preview URL and Publish URL.
