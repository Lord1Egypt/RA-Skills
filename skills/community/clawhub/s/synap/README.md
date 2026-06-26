# synap

Sovereign AI knowledge infrastructure for agents. Typed entity graph, documents, long-term memory, messaging relay, and governance — all backed by PostgreSQL.

## Install

```bash
openclaw skill install synap
```

## What It Does

| Capability        | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| **Entities**      | Typed objects (tasks, people, projects, companies) with properties |
| **Documents**     | Long-form Markdown (reports, summaries, notes)                     |
| **Facts**         | Atomic knowledge across sessions ("Marc prefers email")            |
| **Relations**     | Entity-to-entity links (knowledge graph)                           |
| **Search**        | Full-text + semantic search across everything                      |
| **Message Relay** | Telegram, WhatsApp, Slack, Discord → Synap channels                |
| **A2AI**          | Agent-to-agent communication with Synap Intelligence               |
| **Governance**    | All writes auditable, reversible, proposal-based                   |

## Setup

### Self-Hosted (Free)

```bash
git clone https://github.com/synap-core/backend && cd backend/deploy
cp .env.example .env
docker compose up -d
# Visit https://your-domain/registration to create account
./setup-openclaw.sh
openclaw skill install synap
```

### Managed Pod (15/mo)

1. Sign up at [synap.live](https://synap.live)
2. Settings > API Keys > Create key (`hub-protocol.read` + `hub-protocol.write`)
3. Set `SYNAP_HUB_API_KEY` and `SYNAP_POD_URL` in your environment
4. `openclaw skill install synap`

## Environment Variables

| Variable              | Required | Description                         |
| --------------------- | -------- | ----------------------------------- |
| `SYNAP_HUB_API_KEY`   | Yes      | Hub Protocol API key                |
| `SYNAP_POD_URL`       | Yes      | Synap pod URL                       |
| `SYNAP_WORKSPACE_ID`  | Auto     | Auto-fetched via config endpoint    |
| `SYNAP_AGENT_USER_ID` | Auto     | Auto-fetched via config endpoint    |
| `SYNAP_CONFIG_URL`    | No       | Config pull endpoint (managed pods) |

## Architecture

```
OpenClaw Agent → Hub Protocol REST (/api/hub/*) → Synap Pod
                 Bearer: SYNAP_HUB_API_KEY        PostgreSQL + Typesense + pgvector
```

76+ REST endpoints. Standard HTTP + JSON. No MCP required.

## Replaces

This skill combines and replaces the previous `synap-memory` and `synap-os` skills.
No need to install them separately — `synap` includes everything.

## Links

- [Synap](https://synap.live) — Sovereign AI knowledge infrastructure
- [Hub Protocol](https://synap.live/docs/hub-protocol) — Open REST API spec
- [GitHub](https://github.com/synap-core/backend) — Source code

## License

MIT
