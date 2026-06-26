---
name: Session Memory & Summarization
slug: session-context
description: "Automatically loads recent conversation memory into new sessions and generates AI summaries during compaction to maintain continuity across conversations. Preserves the last 10 raw messages verbatim so the agent can resume exactly mid-conversation without paraphrasing loss."
author: "AniBot (Thomas)"
version: "0.2.0"
license: "MIT"
tags:
  - "memory"
  - "session"
  - "summarization"
  - "continuity"
  - "ai"
hooks:
  - "session:start"
  - "session:compact:before"
repository: "https://github.com/animo66/openclaw-skills"
homepage: "https://clawhub.ai/skills/session-context"
minOpenClawVersion: "0.29.0"
---

# Session Memory & Summarization Skill

Provides automatic conversation continuity across sessions by loading recent memory at session start and generating AI summaries during compaction.

## What It Does

- **Memory Loading**: Injects the latest AI summary AND the last 10 raw message turns verbatim so you resume exactly where you left off
- **AI Summarization**: Generates concise summaries when approaching token limits, written to daily memory files
- **Raw Continuity**: Stores the last N exact interactions alongside the summary so nothing is lost in translation
- **Seamless Experience**: No manual intervention required — just natural conversation flow

## Hooks

### `session:start`

Runs when a new session begins. Loads the most recent daily memory file and injects two context blocks:

1. **AI summary block** — distilled summaries from today + yesterday (up to 6000 chars)
2. **Recent messages block** — last 10 raw user/assistant turns, verbatim, so the AI can resume mid-conversation with exact phrasing and decisions intact

### `session:compact:before`

Runs before automatic compaction (20+ messages OR 60% of token limit). Does two things:

1. Generates an AI summary via `agent.generateSummary()` and prepends it to today's memory file
2. Captures the last 10 user/assistant turns as a JSON block at the end of the file (under `<!-- recent_messages_block -->`) — this is what `session:start` reads back next session

## Installation

```bash
clawhub install session-context
```

Or manually:

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/thomasmarcel/openclaw-skill-session-context.git session-context
openclaw skills enable session-context
```

## Requirements

- OpenClaw ≥ 0.29.0
- Workspace with `memory/` directory (created automatically)
- Access to agent's LLM for summarization

## Configuration

Customize thresholds in `hooks/session/compact:before/handler.js`:

```js
return (
  msgCount >= 20 ||           // minimum messages before summarizing
  tokenCount > maxTokens * 0.6 // trigger at 60% of token limit
);
```

Adjust how many raw messages to preserve:

```js
// In both handler files:
const MAX_RECENT_MESSAGES = 10;  // last N user/assistant turns to preserve verbatim
```

Adjust summary context size:

```js
// In hooks/session/start/handler.js:
const MAX_SUMMARY_CHARS = 6000;  // cap on AI summary injected at session start
```

## Memory Structure

```
memory/
  2026-04-03.md  # daily files — summaries at top, recent_messages block at bottom
  2026-04-04.md
```

Each file has this structure:

```
## HH:MM:SS
<AI summary of the session>

---

## Earlier timestamp
<earlier summary>

<!-- recent_messages_block -->
[{"role":"user","content":"..."},
 {"role":"assistant","content":"..."},
 ...]
```

The `<!-- recent_messages_block -->` section is always at the end and replaced each compaction with the latest N turns.

## How It Works

1. **During a conversation**: As token usage grows, OpenClaw monitors session size.
2. **Before compaction**: The `session:compact:before` hook checks thresholds. If met:
   - Generates an AI summary and prepends it to `memory/YYYY-MM-DD.md`
   - Captures the last 10 raw message turns as a JSON block at the end of the file
3. **Compaction proceeds**: Older messages are pruned.
4. **Next session**: The `session:start` hook loads the file and injects both:
   - The AI summary (for high-level context)
   - The raw recent messages (to resume exactly where you left off)

## License

MIT
