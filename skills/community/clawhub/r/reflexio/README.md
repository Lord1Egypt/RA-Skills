# Reflexio Embedded

Openclaw plugin for user profile and playbook extraction — learns your preferences, corrections, and workflows across sessions using Openclaw's native memory engine, hooks, and sub-agents. No Reflexio server required.

## Prerequisites

- [Openclaw CLI](https://docs.openclaw.ai) (>= 2026.3.24)
- Node.js

## Install

```bash
# 1. Install and enable the plugin
openclaw plugins install /path/to/this/directory
openclaw plugins enable reflexio-embedded

# 2. Enable the active-memory plugin (required for memory search)
openclaw plugins enable active-memory
openclaw config set plugins.entries.active-memory.config.agents '["*"]'

# 3. Register .reflexio/ as a memory search path
openclaw config set agents.defaults.memorySearch.extraPaths '[".reflexio/"]' --strict-json

# 4. Restart the gateway to pick up changes
openclaw gateway restart
```

Verify it loaded:

```bash
openclaw plugins inspect reflexio-embedded
```

## Uninstall

```bash
# 1. Remove the plugin
openclaw plugins disable reflexio-embedded
openclaw plugins uninstall --force reflexio-embedded

# 2. Clean up state files
rm -f ~/.openclaw/reflexio-consolidation-state.json

# 3. Restart the gateway
openclaw gateway restart
```

Your `.reflexio/` user data (profiles and playbooks) is preserved by default. To remove it:

```bash
rm -rf .reflexio/
```

## What it does

- **Profile extraction** — automatically captures user preferences, facts, and corrections from conversations into `.reflexio/profiles/`
- **Playbook capture** — records recurring workflows and patterns into `.reflexio/playbooks/`
- **Dedup and contradiction resolution** — new entries are compared against existing ones via LLM; overlapping content is merged, contradictions resolved (new wins), and non-contradicted facts preserved
- **Consolidation** — periodic heartbeat-triggered sweep that clusters similar entries and merges duplicates
- **TTL management** — profiles can have time-to-live values; expired entries are swept automatically

## Configuration

Override defaults in your `openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "reflexio-embedded": {
        "config": {
          "dedup": { "shallow_threshold": 0.4, "top_k": 5 },
          "consolidation": { "threshold_hours": 24 }
        }
      }
    }
  }
}
```

## Learn more

Full project source, design docs, and development setup:
https://github.com/ReflexioAI/reflexio/tree/main/reflexio/integrations/openclaw-embedded
