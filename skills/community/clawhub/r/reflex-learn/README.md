# ReflexLearn

> **The OpenClaw skill that turns silence into signal.**  
> No ratings. No feedback buttons. Just pure implicit learning from how users actually behave.

![ReflexLearn demo](https://placehold.co/800x400/1a1a2e/00d4ff?text=ReflexLearn+Demo+GIF+%E2%80%94+replace+with+animated+GIF)

[![Version](https://img.shields.io/badge/version-1.1.0-blue)](SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Lines](https://img.shields.io/badge/lines-300-brightgreen)](reflex_learn.py)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-orange)](https://openclaw.ai)

---

## What It Does

Every time a user repeats a similar question, ReflexLearn infers the previous answer failed — and writes a structured reflection to `MEMORY.md`. Every time a question is *not* repeated, it writes a positive reinforcement entry. No explicit feedback required. Ever.

**v1.1.0** adds critical safeguards that make this production-ready:

- **Multi-repeat threshold**: Requires 2+ repeats before flagging failure (avoids false positives from natural follow-ups)
- **Modifier detection**: "Write a Python script to parse JSON **with type hints**" is treated as *preference extraction*, not failure
- **Tiered memory**: In `cautious` mode (default), SOUL.md updates are staged in `reflexlearn-pending.md` for your review before being applied
- **Aggressive mode**: For power users who want instant SOUL.md writes on first confirmed failure
- **Slash commands**: `/reflex status` and `/reflex ignore-last` for manual control

---

## Before / After

**Before ReflexLearn:**

```
User: "Explain async/await in Python"
Agent: [gives a wall of text with no examples]
User: "Explain async/await in Python"   ← agent has no idea this was bad
Agent: [same wall of text again]
```

**After ReflexLearn:**

```
User: "Explain async/await in Python"
Agent: [gives a wall of text with no examples]
→ ReflexLearn logs interaction, signal=neutral

User: "Explain async/await in Python"
→ ReflexLearn: Repeat #1/2 (sim=0.9821) — watching

User: "Explain async/await in Python"
→ ReflexLearn: *** FAILURE SIGNAL *** Repeat threshold reached
→ MEMORY.md: "User repeated 'Explain async/await' 2+ times — previous answer insufficient."
→ reflexlearn-pending.md: "Proposed: improve:explain-async-await — add examples and clarity"

Agent (next session): [reads MEMORY.md, gives concise answer with code examples]
User: satisfied — doesn't repeat the question
→ ReflexLearn heartbeat: Positive reinforcement written
→ SOUL.md: "keep:explain-async-await — user satisfied, maintain this style"
```

**Modifier detection (intentional refinement, NOT flagged as failure):**

```
User: "Write a Python script to parse JSON"
Agent: [writes script without type hints]
User: "Write a Python script to parse JSON with type hints"
→ ReflexLearn: Modifier detected ("with type hint") → preference extraction
→ MEMORY.md: "User prefers Python scripts with type hints"
→ reflexlearn-pending.md: "Proposed: pref:with-type-hint — user prefers type hints"
```

---

## Installation

**Just add to `soul.md`:**

```markdown
## Skills
- reflex-learn
```

**Manual install:**

```bash
# 1. Copy skill folder
mkdir -p ~/.openclaw/skills/reflex-learn
cp -r /path/to/ReflexLearn/* ~/.openclaw/skills/reflex-learn/

# 2. Install dependencies
pip install -r ~/.openclaw/skills/reflex-learn/requirements.txt

# 3. Test it
python3 reflex_learn.py --query "Hello world"
python3 reflex_learn.py --query "Hello world"
python3 reflex_learn.py --query "Hello world"
# → Triggers FAILURE SIGNAL on 3rd run (repeat_count=2 >= threshold=2)

# 4. Check results
cat ~/.openclaw/MEMORY.md
cat ~/.openclaw/reflexlearn-pending.md
```

---

## Configuration

Open `SKILL.md` and edit the config block:

```
SIMILARITY_THRESHOLD: 0.85       # How similar = "same question" (0.0–1.0)
LOOKBACK_INTERACTIONS: 10        # How many past queries to check
POSITIVE_REINFORCEMENT_DELAY: 3  # Interactions to wait before confirming success
REPEAT_COUNT_THRESHOLD: 2        # Repeats needed before flagging failure
SESSION_WINDOW_MINUTES: 60       # Time window for counting repeats
MODE: cautious                   # "cautious" (safe) or "aggressive" (instant writes)
```

**Cautious mode** (default): Proposed SOUL.md updates are written to `~/.openclaw/reflexlearn-pending.md`. Review and approve them by moving entries to `SOUL.md`.

**Aggressive mode**: Updates are written directly to `SOUL.md` on first confirmed failure. Best for users who trust the signal and want fully automated learning.

---

## Slash Commands

| Command | Effect |
|---|---|
| `/reflex status` | Show interaction count, current config, pending review count |
| `/reflex ignore-last` | Remove the last logged interaction (useful after test queries) |

---

## Signal Reference

| Signal | Trigger | Action |
|---|---|---|
| `neutral` | No similar query in history | Log interaction only |
| `watching` | Similar query, below repeat threshold | Log with `watching` signal |
| `preference` | Similar query + modifier words detected | Extract preference → MEMORY.md + pending |
| `negative` | Repeat threshold reached | Reflection → MEMORY.md + pending (or SOUL.md in aggressive) |
| `reinforced` | Query not repeated in next N interactions | Reinforcement → MEMORY.md + SOUL.md |

---

## Optional: Ollama Integration

For richer, AI-generated reflections (requires [Ollama](https://ollama.ai) running locally):

```bash
python3 reflex_learn.py --query "your query" --use-ollama --ollama-model llama3
```

If Ollama is unavailable, ReflexLearn falls back to a structured local reflection automatically.

---

## File Reference

| File | Purpose |
|---|---|
| `~/.openclaw/MEMORY.md` | All reflections and reinforcements (always written) |
| `~/.openclaw/SOUL.md` | Learned patterns (aggressive mode or after manual approval) |
| `~/.openclaw/reflexlearn-pending.md` | Staged updates awaiting review (cautious mode) |
| `~/.openclaw/reflex_history.json` | Interaction history with embeddings (internal) |

---

## Submitting to ClawHub

1. Push this folder to a public GitHub repo: `skills/<your-username>/reflex-learn/`
2. Submit a PR to [openclaw/skills](https://github.com/openclaw/skills)
3. Add an entry to [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills):
   ```markdown
   - [reflex-learn](link) - Turns query repetition into implicit feedback for continuous learning.
   ```

---

## License

MIT — see [LICENSE](LICENSE).
