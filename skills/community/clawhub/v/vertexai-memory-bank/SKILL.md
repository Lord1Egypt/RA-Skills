---
name: vertexai-memorybank
description: >
  Install and configure the OpenClaw Vertex AI Memory Bank plugin for persistent,
  cross-agent memory. Use when the user wants long-term memory, cross-session recall,
  or shared memory across agents. Handles GCP setup, plugin installation, and
  openclaw.json configuration.
license: Apache-2.0
compatibility: Requires Node.js, npm, Google Cloud SDK (gcloud), and a GCP project with Vertex AI enabled.
metadata:
  author: Shubhamsaboo
  version: "1.0.0"
  repository: https://github.com/Shubhamsaboo/openclaw-vertexai-memorybank
---

# Vertex AI Memory Bank Plugin

Give your OpenClaw agent persistent, cross-agent memory powered by Google's Vertex AI Memory Bank.

## What This Does

After setup, your agent will:
- **Auto-recall**: Before each turn, relevant memories are retrieved and injected into context
- **Auto-capture**: After each turn, facts are extracted and stored automatically
- **File sync**: Workspace files (MEMORY.md, USER.md, SOUL.md) sync to Memory Bank with hash tracking
- **Cross-agent**: Tell one agent something, all agents remember it

## Prerequisites

Before running the setup script, ensure:

1. **Google Cloud SDK** installed and authenticated (`gcloud auth application-default login`)
2. **A GCP project** with billing enabled
3. **Vertex AI API** enabled on the project
4. **Node.js 18+** and npm installed

If the user doesn't have these, help them set up each one.

## Installation

Run the setup script:

```bash
bash scripts/setup.sh
```

This script will:
1. Check for required tools (gcloud, npm, node)
2. Prompt for GCP project ID and region
3. Create a Vertex AI Agent Engine reasoning engine (Memory Bank instance)
4. Install the npm plugin package
5. Add the plugin configuration to openclaw.json
6. Restart the gateway to load the plugin

## Manual Installation

If the script doesn't work for your environment, follow these steps:

### Step 1: Create a Memory Bank Instance

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Create a reasoning engine for Memory Bank
curl -X POST \
  "https://REGION-aiplatform.googleapis.com/v1beta1/projects/YOUR_PROJECT_ID/locations/REGION/reasoningEngines" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"display_name": "openclaw-memory-bank"}'
```

Note the reasoning engine ID from the response.

### Step 2: Install the Plugin

```bash
cd /path/to/openclaw-vertex-memorybank
npm install
npm run build
```

### Step 3: Configure openclaw.json

Add to your `openclaw.json` under `plugins`:

```json
{
  "plugins": {
    "openclaw-vertex-memorybank": {
      "enabled": true,
      "path": "/path/to/openclaw-vertex-memorybank",
      "config": {
        "projectId": "YOUR_PROJECT_ID",
        "location": "us-central1",
        "reasoningEngineId": "YOUR_REASONING_ENGINE_ID"
      }
    }
  }
}
```

### Step 4: Restart

```bash
openclaw gateway restart
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `projectId` | required | GCP project ID or number |
| `location` | required | GCP region (e.g. us-central1) |
| `reasoningEngineId` | required | Agent Engine reasoning engine ID |
| `autoRecall` | true | Retrieve memories before each turn |
| `autoCapture` | true | Store memories after each turn |
| `autoSyncFiles` | true | Sync workspace .md files to Memory Bank |
| `autoSyncTopics` | true | Auto-configure memory topics at startup |
| `topK` | 10 | Max memories to retrieve per query |
| `perspective` | "third" | Memory perspective (first or third person) |
| `backgroundGenerate` | true | Fire-and-forget memory generation |
| `ttlSeconds` | none | Auto-expire memories after N seconds |

## Verifying It Works

After installation, check the gateway log:

```bash
tail -f ~/.openclaw/logs/gateway.log | grep memory
```

You should see:
- `[memory-vertex] synced N topics` on startup
- `[memory-vertex] recall: N memories` on each turn
- `[memory-vertex] capture fired (bg)` after each turn

## CLI Commands

The plugin adds these commands:

- `memorybank-search <query>` - Search your memories
- `memorybank-remember <fact>` - Store a specific fact
- `memorybank-forget <memory_id>` - Delete a memory
- `memorybank-sync` - Force sync workspace files
- `memorybank-status` - Check plugin status
- `memorybank-list` - List all stored memories

## Troubleshooting

- **"401 Unauthorized"**: Run `gcloud auth application-default login`
- **"Memory Bank not found"**: Check reasoningEngineId matches your instance
- **No memories recalled**: Check `topK` and `maxDistance` settings. Try `memorybank-search` to verify memories exist
- **High token usage**: Reduce `topK` or set `introspection: "off"` to remove similarity scores

## Source

Full source code and documentation: https://github.com/Shubhamsaboo/openclaw-vertexai-memorybank
