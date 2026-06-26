# OpenClaw Tool Executor

A general-purpose skill for [OpenClaw](https://openclaw.ai) agents that executes tools on any connected third-party service via [Scalekit Connect](https://scalekit.com).

Tell your agent to do something — "get my Notion page", "list HubSpot contacts", "fetch Gmail emails" — and the skill handles the rest: finding the right connection, authorizing if needed, discovering available tools, and executing them.

## How It Works

1. **Discover** — Finds the configured connection for the requested service
2. **Authorize** — Checks if the user is connected; generates a magic link if not
3. **Execute** — Finds the right tool and runs it
4. **Fallback** — If no tool exists, attempts a direct proxied API request

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure credentials

Copy `.env.example` to `.env` and fill in your Scalekit credentials:

```bash
cp .env.example .env
```

```env
TOOL_ENV_URL=https://your-env.scalekit.cloud
TOOL_CLIENT_ID=your_client_id
TOOL_CLIENT_SECRET=your_client_secret
TOOL_IDENTIFIER=your_agent_name
```

Get your credentials from the [Scalekit dashboard](https://app.scalekit.com) under **Developers → API Credentials**.

### 3. Create a connection in Scalekit

You need a connection configured in Scalekit for each service your agent will use.

**Example: Notion**

Follow the [Notion connector setup guide](https://docs.scalekit.com/reference/agent-connectors/notion/) to:
1. Create a Notion OAuth integration
2. Register the redirect URI in Scalekit
3. Add your Notion client ID and secret to the Scalekit dashboard

Once configured, the skill auto-discovers the connection — no hardcoded connection names needed.

## Usage

```bash
# List all connections
uv run tool_exec.py --list-connections

# Filter by provider
uv run tool_exec.py --list-connections --provider NOTION

# Generate auth link (or confirm already connected)
uv run tool_exec.py --generate-link --connection-name notion-xxxx

# List available tools for a provider
uv run tool_exec.py --get-tool --provider NOTION

# Execute a tool
uv run tool_exec.py --execute-tool \
  --tool-name notion_page_get \
  --connection-name notion-xxxx \
  --tool-input '{"page_id": "your-page-id"}'
```

## Supported Providers

Any provider available in Scalekit Connect — Notion, Gmail, Slack, HubSpot, Google Drive, Todoist, and more.

## License

MIT
