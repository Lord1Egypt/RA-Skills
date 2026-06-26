---
name: synapse-layer
description: Persistent memory infrastructure for AI agents with 4-layer Cognitive Security Pipeline (PII redaction, AES-256-GCM encryption, intent validation, differential privacy). Use when: configuring SynapseLayer MCP integration, storing/retrieving agent memories, cross-agent memory sharing, analyzing trust scores, or implementing persistent memory in OpenClaw agents. Also use for troubleshooting SynapseLayer connectivity, understanding Trust Quotient scoring, or setting up framework integrations (LangChain, CrewAI, AutoGen, LlamaIndex, Semantic Kernel).
---

# Synapse Layer Skill

Synapse Layer provides persistent, encrypted memory for AI agents with a 4-layer security pipeline.

## Quick Setup

### Python SDK (Recommended for OpenClaw)

Install and use:

```bash
pip install synapse-layer
```

```python
from synapse_test import SynapseClient

client = SynapseClient(api_key="sk_connect_...")

# Save memory
result = client.remember("User prefers dark mode", agent="mel")

# Retrieve memories
memories = client.recall("user preferences", agent="mel")
```

See [scripts/synapse_client.py](scripts/synapse_client.py) for a complete client implementation.

### MCP Integration (External Tools)

Add to OpenClaw gateway config for external MCP clients:

```json
{
  "mcp": {
    "servers": {
      "synapse-layer": {
        "url": "https://forge.synapselayer.org/mcp",
        "headers": {
          "Authorization": "Bearer sk_connect_YOUR_API_KEY"
        }
      }
    }
  }
}
```

**Note:** This is for external MCP clients (Claude Desktop, Cursor) to connect to SynapseLayer, not for OpenClaw agents to use directly.

## Available Tools

Once configured via Python SDK, these operations are available:

- **save_to_synapse** - Store memory with full security pipeline
- **recall** - Retrieve memories ranked by Trust Quotient™
- **search** - Cross-agent memory search with full-text matching
- **process_text** - Auto-detect decisions, milestones, and alerts
- **health_check** - System health, version, and capability report

## Cognitive Security Pipeline

Every memory passes through 4 non-bypassable layers:

1. **Semantic Privacy Guard™** - 15+ regex patterns detect PII, secrets, credentials
2. **Intelligent Intent Validation™** - Two-step categorization with self-healing
3. **AES-256-GCM Encryption** - Authenticated encryption with PBKDF2 key derivation
4. **Differential Privacy** - Calibrated Gaussian noise on embeddings

## Key Concepts

### Trust Quotient™ (TQ)

Score (0-1) ranking memory reliability. Higher TQ = more trusted memory.

### Cross-Agent Memory

Memories can be shared across agents using the same agent_id or cross-agent search.

### Storage Backends

- **Remote (Forge)** - PostgreSQL via forge.synapselayer.org (recommended)
- **SQLite** - Local .synapse/memories.db (requires local setup)

## Usage Patterns

### Basic Memory Operations

Use the Python SDK client:

```python
from scripts.synapse_client import SynapseClient

client = SynapseClient(api_key="sk_connect_...")

# Save
client.remember("Important decision", agent="mel", importance=5)

# Recall
memories = client.recall("recent decisions", agent="mel", limit=5)

# Search
all_memories = client.search("project deadlines", limit=10)
```

### Process Text Automatically

Extract events from free-form text:

```python
events = client.process_text(
    "Decided to use PostgreSQL. Deadline is May 1st.",
    agent="hermes",
    project="website-redesign"
)
```

## Security Considerations

### Data Privacy

- PII automatically redacted before storage
- All data encrypted at rest (AES-256-GCM)
- Differential privacy protects individual entries
- Zero-knowledge architecture

### Resilience Strategy

**Recommended approach for production:**

1. Use SynapseLayer as primary memory store
2. Keep OpenClaw's MEMORY.md/memory/ as backup
3. Monitor service health via `health_check`
4. Have fallback procedure if service unavailable

## Troubleshooting

### Connection Issues

1. Run `health_check` to verify connectivity
2. Verify API key is valid
3. Check network access to forge.synapselayer.org

### Memory Not Persisting

1. Check API key permissions
2. Verify security pipeline didn't reject content
3. Review Trust Quotient in response

### Low Trust Quotient

1. Review security pipeline logs
2. Increase confidence/importance scores
3. Check if content was sanitized

## Testing

Use the test script:

```bash
python3 /app/skills/synapse-layer/scripts/synapse_test.py
```

This script verifies:
- Service connectivity (health_check)
- Basic save operations
- Memory retrieval
- Cross-agent search

## Reference Documentation

For more details, see:
- [API Reference](references/api.md) - Complete tool documentation
- [Security Details](references/security.md) - Deep dive on security pipeline
- [Framework Integrations](references/integrations.md) - Integration guides
- [Python Client](scripts/synapse_client.py) - Ready-to-use SDK wrapper
