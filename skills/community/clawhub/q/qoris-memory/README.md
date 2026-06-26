# Qoris Memory — Persistent Agent Memory

**Give your OpenClaw agent a memory that survives sessions, branches 
like Git, and scales across your entire team.**

Your agent stops forgetting. Forever.

## Quick Install

```bash
clawhub install qoris-memory
```

Add your credentials:

```bash
export QORIS_API_KEY="your-api-key"
export QORIS_WORKSPACE_ID="your-workspace-id"
```

Get your API key at **qoris.ai/dashboard**

## The Problem It Solves

OpenClaw agents are powerful but amnesiac. Every session starts from
zero. You re-explain context every time. Your agent can't build on
what it learned last week.

Qoris Memory fixes this. Your agent remembers everything — across
sessions, across team members, across projects.

## How It Works

Think GitHub for your agent's brain:

- **Commits** — every memory update is versioned with timestamp and author
- **Branches** — separate memory contexts for different projects
- **Merges** — combine contexts intelligently with conflict resolution
- **Search** — semantic search across everything your agent knows

## What Your Agent Can Do With It

```
# Store a memory
"Remember that Acme Corp prefers weekly reports on Fridays"

# Search knowledge
search_knowledge("what does the client prefer for reporting?")

# Branch for a project
/memory branch create project-alpha

# List all memories
get_memories()
```

## Works Better With Knox

Pair with **knox-governance** (also by qorisai) for fully governed
enterprise agent deployments — every memory read and write logged
in the Knox audit trail.

```bash
clawhub install knox-governance
clawhub install qoris-memory
```

## Free Tier Includes

- 1,000 memories
- 500MB knowledge document storage
- Unlimited semantic search
- Full version history

## Links

- Documentation: https://docs.qoris.ai/memory
- Dashboard: https://qoris.ai/dashboard
- Demo: https://qoris.ai/contact-us
- Support: eliel@qoris.ai

---

Qoris AI · NVIDIA Inception Program · Claude Partner Network
Patent Pending U.S. 63/907,730
