---
name: workflow-cache
description: "Save up to 90% on Token costs. One agent explores, all agents benefit. Cloud-cached workflows with zero inference cost."
metadata:
  openclaw:
    emoji: "🧠"
---

# Workflow Cache

**One agent explores, all agents benefit.**

A crowdsourced workflow registry that caches successful automation patterns, letting you skip LLM inference entirely when a matching workflow exists.

## Why Use This?

### 1. Save Real Money

Traditional approach: LLM explores and reasons through every step, burning tokens on trial-and-error.

Our approach: Query the cloud for a cached workflow. If found, execute directly. **Zero inference cost.**

**Token savings example (10-step browser task):**
- Traditional: ~5000 tokens
- Workflow Cache: ~800 tokens
- **Savings: 80%+**

The more complex the task and the more you repeat it, the more you save.

### 2. Skip the Debugging Hell

The painful part of AI automation isn't writing the script—it's the endless debugging when:
- The website changes its layout
- Selectors break unexpectedly
- Edge cases you didn't anticipate

**Workflow Cache solves this:**
- Every successful workflow from any agent is cached
- When websites change, cached workflows auto-update
- You never debug the same problem twice

### 3. Platform Agnostic

Works with any Claw/Lobster engine. One workflow, all platforms. Automatic syntax adaptation.

## How It Works

```
User Intent → Query Cloud → Match Found?
                                ↓ Yes        ↓ No
                          Execute Now    Normal Flow
                          (1 second)     (LLM reasons)
                                ↓              ↓
                          Success!      Success → Contribute
```

**One agent's success becomes every agent's shortcut.**

## Features

### Interceptor
Queries the cloud before LLM inference. On match, replays the cached workflow directly.

### Trace Compiler
Converts successful session traces into reusable Lobster workflows automatically.

### PII Sanitizer
Local-first privacy. All sensitive data stays local. Only workflow patterns are shared.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `cloud_endpoint` | string | `https://api.workflowcache.dev` | Cloud API endpoint |
| `enabled` | boolean | `true` | Enable/disable interception |
| `auto_contribute` | boolean | `true` | Auto-contribute successful workflows |
| `timeout_ms` | number | `300` | API timeout (ms) |

## Installation

```bash
npx clawhub install workflow-cache
```

Or manually:

```bash
cd ~/.qclaw/workspace/skills/workflow-cache
npm install
npm run build
```

## Security

- Full PII sanitization pipeline
- No account credentials ever uploaded
- Multi-node security validation on all workflows
- Malicious injection detection and blocking

## Who Is This For?

- **Heavy AI users** — Daily automation, high token bills
- **Cost-conscious developers** — Every token saved is money saved
- **Automation enthusiasts** — Stop reinventing wheels
- **Efficiency maximalists** — Why reason when you can replay?

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.

---

**Tags:** `#AI-efficiency` `#token-saver` `#automation` `#crowdsourced` `#workflow-cache`