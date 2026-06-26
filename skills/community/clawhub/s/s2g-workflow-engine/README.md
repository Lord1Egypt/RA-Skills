# S2G — OpenClaw Skill

> Connect OpenClaw agents to [S2G](https://s2g.run) visual workflow automation platform. Execute 200+ workflow nodes as tools over WebSocket — no port forwarding, no public IP required.

## What is S2G?

[S2G](https://s2g.run) ("Just Run It") is a visual workflow automation platform with:

- **200+ integration & data processing nodes** — HTTP, databases, AI models, file operations, cloud connectors
- **AI integration** — OpenAI, Anthropic, Gemini, DeepSeek, Mistral, Groq with built-in prompt management
- **Vector storage** — Built-in vector database for RAG applications
- **Knowledge Base** — Graph-based knowledge store with semantic search, entities, and relations
- **Custom Node Designer** — Create your own nodes with JavaScript logic (sandboxed runtime)
- **HTTP triggers & webhooks** — Public endpoints that start workflows from any external service
- **Visual drag-and-drop editor** — Design workflows with real-time execution visualization
- **AI Workflow Generator** — Describe what you want in natural language, S2G builds the workflow

## What does this skill do?

This skill connects your OpenClaw agent to an S2G workflow via the **OpenClaw node** — a built-in S2G node type that acts as a **bidirectional WebSocket bridge**. Once connected, the agent can:

- **Execute any node** in the workflow as a tool (password generators, hash functions, date math, database queries, AI models, knowledge base operations, and 200+ more)
- **Receive data pushes** from S2G workflows via Input Forwarding (e.g., webhook triggers → data processing → agent notification)
- **Manage workflows** via the REST API (create, start/stop, add nodes, wire connections)
- **Discover node schemas** to learn exact parameter names and types
- **Generate workflows** from natural language via the AI Assistant API

```
OpenClaw ──WS──▶ S2G (wss://s2g.run/api/openclaw/ws/{nodeId})
                   ├── PasswordGenerator
                   ├── HashGenerator
                   ├── DateMath
                   ├── SqlServer / PostgreSQL / MongoDB
                   ├── Knowledge Base (graph store)
                   ├── VectorDb (RAG)
                   ├── OpenAI / Anthropic / Gemini
                   ├── HTTP Listener (webhooks)
                   ├── Cloud connectors (OneDrive, M365)
                   └── ... 200+ node types
```

## Why WebSocket? Key Benefits

### 🔒 No Exposure Required

The bridge makes an **outbound WebSocket connection** from your machine to S2G. This means:

- **No port forwarding** — Your OpenClaw instance stays behind NAT/firewall
- **No public IP needed** — Works from home networks, laptops, corporate environments
- **No reverse proxy setup** — No nginx, no Cloudflare tunnels, no Tailscale funnel
- **No incoming firewall rules** — The connection is initiated by you, not by S2G

Your agent reaches out to S2G — S2G never needs to reach into your network.

### 🌐 Works From Anywhere

Because the connection is outbound, the bridge works from:

- **Home networks** behind consumer routers
- **Corporate environments** behind enterprise firewalls
- **Laptops** on Wi-Fi, mobile hotspots, or VPNs
- **Cloud VMs** without public-facing ports
- **Containers** without host networking

As long as your machine can make outbound HTTPS/WSS connections (port 443), the bridge works.

### 🔄 Persistent & Self-Healing

- **Auto-reconnect** — If the connection drops (network blip, S2G restart, laptop sleep/wake), the bridge reconnects automatically in 5 seconds
- **Keepalive pings** — 30-second heartbeat prevents silent disconnects
- **Stateless** — No session files, no tokens to refresh. Just the host URL and node ID
- **Zero-config recovery** — Wake up your laptop → bridge reconnects → all tools available again

### 🛡️ Secure by Design

- **TLS encrypted** — `wss://s2g.run` uses standard TLS (port 443)
- **Optional auth secret** — Set a shared secret on the OpenClaw node so only authorized bridges can connect
- **No credentials in transit** — The bridge doesn't send your S2G API key over WebSocket; auth is handled by a separate secret
- **Local API only** — The bridge HTTP API (port 18792) runs locally; only your agent accesses it

### ⚡ Real-Time Bidirectional

Unlike REST-only integrations:

- **Agent → S2G**: Execute any node, get results in real-time
- **S2G → Agent**: Push data from workflows to the agent (Input Forwarding)
- **Sub-second latency**: WebSocket stays open — no connection overhead per request
- **Live View**: Watch execute/result pairs flow in real-time in the S2G designer

## Features

- **Auto-discovery** — Connects via WebSocket, discovers all sibling nodes automatically
- **Execute by name** — Fuzzy-matched node execution via local HTTP API
- **Auto-reconnect** — Handles disconnects, restarts, and network blips gracefully
- **Auth support** — Optional secret-based WebSocket authentication
- **Data push** — Receive data from S2G workflows via Input Forwarding and Manual Payload
- **File logging** — Persistent logs with 5MB automatic rotation
- **Full REST API coverage** — Manage workflows, catalog, knowledge base, AI generation programmatically
- **Node schema discovery** — Query exact input/output parameter names before executing

## Install

### Via ClawHub
```bash
clawhub install s2g
```

### Via GitHub URL
Give OpenClaw this repo URL:
```
https://github.com/s2g-run/openclaw-skill
```

### Manual
Copy the `s2g/` folder into your OpenClaw skills directory:
```bash
cp -r s2g/ ~/.openclaw/workspace/skills/s2g/
```

## Quick Start

### 1. Set up S2G

1. Sign up at [s2g.run](https://s2g.run)
2. Create a new workflow
3. Add an **OpenClaw node** (AI category) from the node palette
4. Add tool nodes you want your agent to access (e.g., PasswordGenerator, HashGenerator, DateMath)
5. Connect the OpenClaw node to the tool nodes
6. **Start the workflow** (▶ button)
7. Click the OpenClaw node → copy the **Node ID** (UUID) from properties

### 2. Start the bridge

```bash
# Install dependency
npm install ws

# Copy bridge script to workspace
cp ~/.openclaw/workspace/skills/s2g/scripts/s2g-bridge.js ~/.openclaw/workspace/

# Start the bridge (outbound connection — no port forwarding needed!)
node s2g-bridge.js --s2g wss://s2g.run --node-id YOUR_NODE_UUID --port 18792
```

### 3. Verify & use

```bash
# Check connection
curl http://localhost:18792/health
# {"healthy":true,"uptime":42.5}

# List discovered nodes
curl http://localhost:18792/nodes

# Execute a node
curl -X POST http://localhost:18792/execute/PasswordGenerator \
  -H "Content-Type: application/json" \
  -d '{"params":{"length":"24","mode":"strong"}}'
```

## How It Works

```
┌─────────────────┐         ┌──────────────────────────┐
│   Your Machine  │         │      S2G (s2g.run)       │
│                 │         │                          │
│  ┌───────────┐  │   WSS   │  ┌────────────────────┐  │
│  │  OpenClaw │  │ ──────▶ │  │   OpenClaw Node    │  │
│  │   Agent   │  │ ◀────── │  │  (AI category)     │  │
│  └─────┬─────┘  │         │  └────────┬───────────┘  │
│        │        │         │           │              │
│  ┌─────▼─────┐  │         │  ┌────────▼───────────┐  │
│  │  Bridge   │  │         │  │  Sibling Nodes     │  │
│  │ :18792    │  │         │  │  ├─PasswordGen     │  │
│  └───────────┘  │         │  │  ├─ HashGenerator  │  │
│                 │         │  │  ├─ SqlServer      │  │
│  No open ports! │         │  │  ├─ Knowledge      │  │
│  No public IP!  │         │  │  └─ ... 200+ more  │  │
└─────────────────┘         │  └────────────────────┘  │
                            └──────────────────────────┘
```

1. The bridge opens an **outbound** WebSocket connection to `wss://s2g.run`
2. S2G sends the list of all available nodes in the workflow
3. Your agent calls the bridge's local HTTP API to execute nodes
4. The bridge forwards requests over the WebSocket → S2G executes → results come back
5. S2G can also **push data** to the agent via Input Forwarding (upstream workflow events)

## Prerequisites

1. An S2G account at [s2g.run](https://s2g.run)
2. A workflow with an **OpenClaw node** (found in the AI category) and tool nodes connected to it
3. The workflow must be **running** (▶ Start in designer or `POST https://s2g.run/api/v1/workflows/{id}/start`)
4. Node.js with `ws` module

## Skill Structure

```
s2g/
├── SKILL.md                  — Agent instructions and node reference
├── scripts/
│   └── s2g-bridge.js         — WebSocket bridge server (stateless, auto-reconnect)
└── references/
    ├── api.md                — Full S2G REST API (28 endpoints)
    ├── protocol.md           — WebSocket protocol specification
    └── operations.md         — Deployment, monitoring, and operations guide
```

## API Coverage

All REST API endpoints at `https://s2g.run/api/v1/`. WebSocket bridge at `wss://s2g.run/api/openclaw/ws/{nodeId}`.

| Area | Base URL | Description |
|------|----------|-------------|
| Workflows | `/api/v1/workflows` | Create, start/stop, add/remove nodes and connections (11 endpoints) |
| Catalog | `/api/v1/catalog` | Discover 200+ node types and their exact schemas (4 endpoints) |
| Knowledge Base | via workflow node | Graph store: search, entities, relations (11 operations) |
| AI Assistant | `/api/v1/ai` | Generate workflows from natural language (4 endpoints) |
| Connections | `/api/v1/connections` | OAuth/API key management (5 endpoints) |
| Usage & Logs | `/api/v1/usage` | Quotas, execution counts, node-level logs (4 endpoints) |
| HTTP Listener | `listener.s2g.run` | Webhook triggers for workflows |
| OpenClaw Bridge | `/api/openclaw` | WebSocket endpoint + health check |

## Links

- **S2G Platform:** [https://s2g.run](https://s2g.run)
- **OpenClaw:** [https://github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- **ClawHub:** [https://clawhub.ai](https://clawhub.ai)

## License

MIT
