---
name: reflex-learn
description: Detects repeated queries as implicit negative feedback and non-repetition as positive feedback, enabling continuous learning by writing reflections and patterns to MEMORY.md and SOUL.md. v1.1.1 adds path validation, model-download guard, --offline flag, and a formal install.sh.
version: 1.1.1
triggers:
  - "post-response"
  - "heartbeat"
metadata:
  openclaw:
    requires:
      bins: ["python3", "bash"]
---

# ReflexLearn

ReflexLearn enables true continuous learning via implicit feedback. It turns repetition of the same question into an automatic "I screwed up" signal and non-repetition into a "user is satisfied" signal — with no explicit rating or feedback required from the user.

**v1.1.1 fixes**: path validation enforced in code (all writes restricted to `~/.openclaw/`), model-download guard with explicit warning and `--offline` flag, `install.sh` for declared one-step PyPI + model-weight setup, `scikit-learn` removed from dependencies (was unused).

## Installation

**Step 1 — Run the install script.** This is the only step that touches the network. It installs Python packages from PyPI and pre-caches the model weights from Hugging Face (~80 MB, one-time only). After this step the skill can run fully offline.

```bash
bash {baseDir}/install.sh
```

The script explicitly lists every network operation before proceeding and requires confirmation.

**Step 2 — Add to `soul.md`:**

```markdown
## Skills
- reflex-learn
```

## Usage

Run after every agent response (post-response trigger):

```bash
python3 {baseDir}/reflex_learn.py \
  --query "<current_user_query>" \
  --memory-file ~/.openclaw/MEMORY.md \
  --soul-file ~/.openclaw/SOUL.md \
  --history-file ~/.openclaw/reflex_history.json \
  --pending-file ~/.openclaw/reflexlearn-pending.md \
  --skill-md {baseDir}/SKILL.md \
  --offline
```

Run on heartbeat to scan for positive reinforcement candidates:

```bash
python3 {baseDir}/reflex_learn.py \
  --heartbeat \
  --memory-file ~/.openclaw/MEMORY.md \
  --soul-file ~/.openclaw/SOUL.md \
  --history-file ~/.openclaw/reflex_history.json \
  --skill-md {baseDir}/SKILL.md \
  --offline
```

Optionally, use local Ollama for richer AI-generated reflections (no additional network access — Ollama runs locally):

```bash
python3 {baseDir}/reflex_learn.py --query "<query>" --use-ollama --ollama-model llama3
```

Slash commands (pass as --query value):

```bash
python3 {baseDir}/reflex_learn.py --query "/reflex status"
python3 {baseDir}/reflex_learn.py --query "/reflex ignore-last"
```

## Configuration

Edit these values directly in this file to tune behaviour. They are parsed at runtime.

- SIMILARITY_THRESHOLD: 0.85
- LOOKBACK_INTERACTIONS: 10
- POSITIVE_REINFORCEMENT_DELAY: 3
- REPEAT_COUNT_THRESHOLD: 2
- SESSION_WINDOW_MINUTES: 60
- MODE: cautious

| Option | Default | Description |
|---|---|---|
| `SIMILARITY_THRESHOLD` | `0.85` | Cosine similarity above which two queries are considered the same |
| `LOOKBACK_INTERACTIONS` | `10` | How many past interactions to compare against |
| `POSITIVE_REINFORCEMENT_DELAY` | `3` | Interactions to wait before confirming positive reinforcement |
| `REPEAT_COUNT_THRESHOLD` | `2` | Repeats within the session window required to flag as failure |
| `SESSION_WINDOW_MINUTES` | `60` | Time window (minutes) within which repeats are counted |
| `MODE` | `cautious` | `cautious` = stage updates in pending file; `aggressive` = write directly to SOUL.md |

## Signal Types

| Signal | Meaning |
|---|---|
| `neutral` | No similar query found in history |
| `watching` | Similar query found, repeat count below threshold — monitoring |
| `preference` | Similar query with modifier words — preference extracted, not a failure |
| `negative` | Repeat threshold reached — reflection written to MEMORY.md |
| `reinforced` | Query not repeated in next N interactions — positive reinforcement written |

## Core Behavior

On every user message, ReflexLearn embeds the query with `sentence-transformers` (`all-MiniLM-L6-v2`) and compares it to the last `LOOKBACK_INTERACTIONS` interactions stored in `~/.openclaw/reflex_history.json`.

If cosine similarity > `SIMILARITY_THRESHOLD` and the query contains modifier words (e.g., "be more concise", "add examples", "in table format"), it extracts a preference and writes it to `MEMORY.md` — it does **not** flag this as a failure.

If cosine similarity > `SIMILARITY_THRESHOLD` without modifier words and the repeat count within `SESSION_WINDOW_MINUTES` reaches `REPEAT_COUNT_THRESHOLD`, it triggers a reflection and writes it to `MEMORY.md`.

In `cautious` mode (default), proposed SOUL.md updates are staged in `reflexlearn-pending.md` for human review. In `aggressive` mode, they are written directly to SOUL.md.

On heartbeat, if the same query is NOT repeated in the next `POSITIVE_REINFORCEMENT_DELAY` interactions, it triggers positive reinforcement.

All memory writes are valid Markdown that OpenClaw already understands.

## Security and Network Rules

- **Path enforcement**: The code resolves all file paths and aborts with an error if any path falls outside `~/.openclaw/`. This is enforced in code, not just documentation.
- **No runtime network access**: After `install.sh` has been run, the skill operates fully offline when invoked with `--offline`. Without `--offline`, a warning is printed if the model is not cached.
- **Declared network operations**: All network access (PyPI, Hugging Face) is performed exclusively by `install.sh`, which lists operations and requires user confirmation before proceeding.
- **Local Ollama only**: The optional Ollama integration calls `localhost:11434` only — no external API.
- **No writes outside `~/.openclaw/`**: Enforced at runtime; any misconfigured path triggers an immediate exit.
- In cautious mode, NEVER write directly to SOUL.md without staging in pending file first.
