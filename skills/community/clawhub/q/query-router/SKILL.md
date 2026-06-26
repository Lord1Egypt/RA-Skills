---
name: query-router
description: >-
  Unified query router combining content-type detection, complexity scoring, and
  prefix-based routing. Routes queries to the optimal model with safety features
  (lock protection, verify-after-switch, rollback, audit logs).
  Use when: route this query, which model should I use, classify this, route to
  optimal model, query type, auto-select model, @codex, @mini, @cl, @q.
---

# Query Router

Routes every query to its best-fit model using three routing strategies combined:

1. **Prefix routing** — explicit user intent (`@codex`, `@mini`, etc.)
2. **Content-type detection** — auto-detect vision/voice/tool/code/reasoning/qa
3. **Complexity scoring** — simple/moderate/complex tier routing

## Usage

### Classify only

```bash
python3 skills/query-router/scripts/classify.py [--json] [--attachment .ext] <query>
```

### Route (classify + switch model)

```bash
python3 skills/query-router/scripts/router.py [--json] [--dry-run] [--attachment .ext] <query>
```

### Safety & Audit

```bash
python3 skills/query-router/scripts/router.py --check           # list available models
python3 skills/query-router/scripts/router.py --audit            # show recent routing log
python3 skills/query-router/scripts/router.py --no-lock          # disable lock protection
python3 skills/query-router/scripts/router.py --dry-run --no-verify  # preview without verify
```

### Library usage

```python
from router import route_query

result = route_query(
    query="@codex write a complex python script",
    has_attachment=False,
    attachment_ext="",
    dry_run=True,       # True = preview, False = actually switch
    enable_lock=True,   # prevent concurrent routing
    enable_verify=True, # readback verify after switch
    enable_rollback=True,  # revert on failure
)
print(result["action"])        # route | recommend | skip | blocked
print(result["to_model"])      # recommended model name
print(result["classification"]) # full classification details
```

## Routing Priority

| Priority | Signal | Example | Behavior |
|----------|--------|---------|----------|
| 1 | **Prefix** | `@codex write a script` | Force switch to `@codex` model |
| 2 | **Content-type** (≥60%% conf) | `describe this image` | Auto-switch to vision model |
| 3 | **Complexity** (<60%% conf) | `analyze Q3 data` | Route by complexity tier |
| 4 | **Skip** (<30%% conf) | `hi how are you` | Keep current model |

## Prefix Routing

| Prefix | Model | Aliases |
|--------|-------|---------|
| `@codex` | `openai-codex/gpt-5.3-codex` | `@c` |
| `@mini` | `minimax-m2.7:cloud` | Cloud primary |
| `@cl` | `qwen3-coder-next:cloud` | Cloud code |
| `@q` | `minimax-m2.7:cloud` | Cloud fast Q&A |
| `@llava` | `qwen3.5:cloud` | Cloud vision |
| `@whisper` | `whisper` | — |

## Content Types

| Type | Detected By | Best Model |
|------|-------------|------------|
| **vision** | Image attachment or "describe/identify" | qwen3.5:cloud |
| **voice** | Audio file or "transcribe/speech-to-text" | whisper |
| **tool** | run, fetch, send, check, sync | minimax-m2.7:cloud |
| **code** | script, function, import, debug | qwen3-coder-next:cloud |
| **reasoning** | analyze, compare, plan, think | minimax-m2.7:cloud |
| **qa** | what is, how does, define | minimax-m2.7:cloud |

## Complexity Tiers

| Tier | Pattern | Model |
|------|---------|-------|
| **simple** | greetings, one-liners, short questions | minimax-m2.7:cloud |
| **moderate** | emails, analysis, search, translate | minimax-m2.7:cloud |
| **complex** | multi-file code, deep research, architect | minimax-m2.7:cloud |

## Safety Features

- **Lock protection** — prevents concurrent routing ops (`fcntl`)
- **Verify-after-switch** — confirms model actually changed
- **Rollback** — reverts to previous model on failure
- **Audit log** — JSONL log at `scripts/.logs/router.log.jsonl`

## Merged Approaches

| Source | Technique |
|--------|-----------|
| `openclaw-model-router-skill` | Prefix syntax `@codex/@mini`, lock + verify + rollback |
| `task-complexity-router` | Complexity tier scoring (simple/moderate/complex) |
| `query-router` (original) | Content-type detection (vision/voice/tool/code/qa) |

All three combined into one unified router with confidence-based priority.
