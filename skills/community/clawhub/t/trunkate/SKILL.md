---
name: "trunkate-ai"
description: >
  Semantically optimizes context history and large text blocks via the Trunkate AI API. 
  Includes proactive context pruning hooks for automated token management.
version: "0.29.0"
author: "Trunkate"
homepage: "https://trunkate.ai"
repository: "https://github.com/Trunkate-AI/trunkate-ai-skills"
bugs: "https://github.com/Trunkate-AI/trunkate-ai-skills/issues"
bins: ["python3"]
os: ["linux", "darwin"]
scripts: true
requires:
  bins: ["python3"]
  env: ["TRUNKATE_API_KEY", "OPENCLAW_HISTORY_PATH", "OPENCLAW_CURRENT_TOKENS", "OPENCLAW_TOKEN_LIMIT"]
  optional_env: ["OPENCLAW_LAST_ERROR_MESSAGE", "TRUNKATE_THRESHOLD", "TRUNKATE_AUTO_BUDGET", "TRUNKATE_API_URL", "TRUNKATE_DEBUG"]
install:
  - id: pip
    kind: shell
    command: pip install -r requirements.txt
    bins: ["python3"]
    label: Install Python dependencies
---

# Trunkate AI Skill

Semantic context optimization and automated history pruning. Trunkate AI ensures high-density reasoning by semantically compressing text via the private Trunkate API, preserving core logic and project facts while stripping redundant boilerplate, repetitive logs, and low-signal conversation turns.

## Quick Reference

| Situation | Action |
| ----------- | -------- |
| Systematic Precision | `PreRequest` hook triggers `scripts/activator.py` on every call |
| Massive file/log ingestion | Run: `trunkate --text "$(cat log.txt)" --budget "20%"` |
| Context overflow error | System triggers `scripts/error-detector.py` for emergency wipe |
| High token costs / Latency | Proactive "Smart Buffer" maintains constant context density |
| Critical facts preservation | Wrap blocks in `[KEEP] ... [/KEEP]` tags for 100% fidelity |
| Private/sensitive data | Wrap in `[PRIVATE] ... [/PRIVATE]` tags — never sent to API |
| Review performance ROI | Check `references/examples.md` for semantic fidelity metrics |
| Multi-agent context handoff | Condense context before spawning sub-agents via `sessions_spawn` |
| Focus pivoting | Use manual prune with `--task` to reset reasoning attention |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automated lifecycle hooks for background memory management.

### Installation

**Via ClawdHub (recommended):**

```bash
clawdhub install trunkate-ai
```

**Manual:**

```bash
git clone https://github.com/Trunkate-AI/trunkate-ai-skills.git ~/.openclaw/skills/trunkate-ai
```

### Skill Structure

Trunkate AI follows a standardized event-driven architecture to ensure high reliability and low latency:

```bash
trunkate-ai/
├── assets/                     # Project initialization templates
│   └── TRUNKATE_RULES.md       # User rules for "Never-Prune" blocks
├── hooks/                      # Active lifecycle hooks
│   └── openclaw/
│       ├── HOOK.md             # Technical documentation for hooks
│       └── pre_request.py      # THE HOOK: Intercepts outgoing LLM calls
├── references/                 # Technical standards and guides
│   ├── examples.md             # API usage examples (Before/After)
│   ├── hooks-setup.md          # Integration guide for Python hooks
│   └── openclaw-integration.md # Mapping of OpenClaw variables
├── scripts/                    # Core executable logic
│   ├── activator.py            # Main entry point (Proactive Systematic Hook)
│   ├── error_detector.py       # Reactive hook for context failures
│   └── trunkate.py             # Core API client (Python Native)
├── SKILL.md                    # This file
├── requirements.txt            # Dependencies (requests)
└── version.txt                 # Version tracking
```

### Initialize Optimization Rules

To protect specific files or data blocks from being sent to the API, customize the local rules template:

```bash
cp assets/TRUNKATE_RULES.md assets/MY_PROJECT_RULES.md
```

---

## Optimization Strategy

Trunkate AI applies a semantic preservation hierarchy to ensure you never lose critical project requirements during compression.

### Preservation Hierarchy (Protected Context)

| Content Type | Preservation Priority | Strategy |
| --- | --- | --- |
| **Atomic Blocks** | **Critical** | 100% Verbatim; wrap in `[KEEP] ... [/KEEP]` tags |
| **Private Data** | **Critical** | 100% Verbatim; wrap in `[PRIVATE] ... [/PRIVATE]` tags. Content never leaves the client — replaced with `__PRIVATE_N__` placeholders before API transmission. |
| **System Instructions** | **Critical** | 100% Verbatim for `<system>` tags; stripped locally before transmission |
| **Active Task/Goal** | **High** | Full fidelity retention of current user intent |
| **Project Facts** | **High** | Core conventions and facts (e.g. from CLAUDE.md) |
| **Recent Turns** | **High** | Verbatim retention of the last 3-5 conversation turns |
| **Logic Blocks** | **Medium** | Semantic compression via Trunkate API |
| **Large Logs/Dumps** | **Low** | Summary transformation (extracting error patterns) |
| **Boilerplate** | **None** | Aggressive pruning of license headers and noise |

---

## Hook Integration

Trunkate AI is designed for automated background operation via triggers. Configure these in your OpenClaw settings to explicitly enable memory management as a background utility. Note that enabling the PreRequest hook will automatically transmit your OpenClaw session history to api.trunkate.ai.

### Proactive Trigger (PreRequest)

Configure this in `.openclaw/config.json` to prune history BEFORE every LLM call. This is the primary method for maintaining "Always-On" context efficiency.

**Hook Config:**

```json
{
  "hooks": {
    "PreRequest": [
      {
        "type": "command",
        "command": "python3 hooks/openclaw/pre_request.py"
      }
    ]
  }
}
```

### Error Detector (OnError)

Triggers on context failures (e.g., 429 or 400 errors from the model) to perform emergency history wipes.

**Error Config:**

```json
{
  "hooks": {
    "OnError": [
      {
        "type": "command",
        "command": "python3 scripts/error_detector.py"
      }
    ]
  }
}
```

---

## Logging & ROI Tracking

When manual or proactive pruning occurs, a summary of the action should be logged to ensure traceability.

### Optimization Log Entry

Append significant optimizations to a local tracking file for review:

## [TRK-YYYYMMDD-XXX] Category (e.g., proactive_prune | manual_summarization)

**Logged**: ISO-8601 timestamp
**Original Size**: Token count before optimization
**Optimized Size**: Token count after optimization
**ROI**: Percentage reduction (e.g., 85%)
**Trigger**: Proactive threshold | Context Error | Manual Call

### Summary

One-line description of the optimized content (e.g., "Pruned 15 turns of build logs")

### Preserved State

List of critical facts or logic blocks that were protected via [KEEP], [PRIVATE], or Rules.

### suggested_budget_update

If reasoning quality dropped, suggest increasing TRUNKATE_AUTO_BUDGET.

---

## Detection Triggers

Automatically trigger `trunkate` or advise the user to adjust the `TRUNKATE_THRESHOLD` when you notice these signals.

### Cognitive Load (Internal Signals)

* "I am repeating previous mistakes despite direct user corrections..."
* "I've forgotten primary project facts (e.g., which package manager to use)..."
* "The conversation history is 90% repetitive logs or stack traces..."
* "I'm having trouble focusing on the core logic due to context noise..."
* "I am hallucinating file paths or variable names that do not exist..."

### Massive Ingestion (External Signals)

* Reading a 10,000-line stack trace from a build failure.
* Analyzing a full `npm install` or `pip install` output.
* Parsing a large database schema or raw SQL dump.
* Processing raw data exports or multi-megabyte JSON payloads.

---

## Environment Variables

| Variable | Requirement | Purpose |
| --- | --- | --- |
| `TRUNKATE_API_KEY` | **REQUIRED** | Authentication for api.trunkate.ai. |
| `TRUNKATE_THRESHOLD` | Optional | Context usage % before trigger (e.g. 0.8 for 80%). |
| `TRUNKATE_AUTO_BUDGET` | Optional | Target for optimized history (e.g., 2000 or "20%"). |
| `TRUNKATE_API_URL` | Optional | Override default for local testing or dev environments. |
| `TRUNKATE_DEBUG` | Optional | Enable verbose logging of hook execution to console. |

---

## Best Practices

1. **Background Operation**: Truncation runs as an infrastructure task. Transparency is maintained via log files.
2. **Contextual Tasking**: When calling manually, use `--task` to guide the semantic summarizer (e.g. "Focus on the auth handler logic").
3. **Protect Critical Files**: Update `TRUNKATE_RULES.md` whenever you add a new foundational file or secret environment variables.
4. **Log Immediately**: If a large tool output is generated, trunkate it before it gets buried and degrades the next reasoning step.
5. **Recursive Handling**: If a block remains too large, truncate sub-modules individually before a final consolidation.
6. **Task Pivoting**: Use `trunkate` with a new task description to clear your "mental workspace" when shifting from backend to frontend.

---

## Integration with Multi-Agent Workflows

When spawning sub-agents (e.g., via OpenClaw `sessions_spawn`), use Trunkate to optimize the hand-off context:

1. Run `trunkate` on the primary context with a task specific to the sub-agent's goal.
2. Pass the high-density optimized context as the initial prompt to the sub-agent.
3. This ensures the sub-agent has the maximum possible token space for its specialized task.

## Periodic Review

Review the performance metrics and technical standards at natural breakpoints:

* **Before major tasks**: Check if history is too stale or noisy via `references/examples.md`.
* **After feature completion**: Evaluate the token efficiency ROI in your logs.
* **Weekly**: Tune the `TRUNKATE_THRESHOLD` based on your model's recent reasoning performance.

---

## Safety Boundaries & Permissions

To comply with OpenClaw automated health/safety grades:

* **Safety Boundaries**: When performing shell execution (`exec`) to run local Python scripts (such as `activator.py` or `.openclaw` hooks), the skill is strictly restricted to semantic compression and logging. The hook execution environment is whitelisted (minimized) to only pass necessary `TRUNKATE_*` and `OPENCLAW_*` variables, preventing unauthorized access to other workspace secrets. It contains safety boundaries to ensure it does not execute unknown payloads, access external network resources (other than api.trunkate.ai for optimization), or execute arbitrary code. **Privacy**: Content wrapped in `[PRIVATE]…[/PRIVATE]` tags is automatically extracted locally and replaced with `__PRIVATE_N__` placeholders before any API call — the original private data never leaves your machine. Additionally, `[KEEP]` blocks, `<system>` tags, `.env` markdown blocks, and regex-detected secrets are also stripped locally. Note that the regex-based auto-detection may not catch all generalized secrets; use explicit `[PRIVATE]` tags for guaranteed protection.
* **Permissions**: This skill **does not** require "Human-in-the-loop" approval because it does not perform destructive actions (like deleting tickets or pushing code). It operates purely on localized context and data streams.

---

*Trunkate AI: Ensuring your context window is always secure, lean, dense, and effective.*
