# Session Memory & Summarization

Automatically loads recent conversation memory into new sessions and generates AI summaries during compaction to maintain continuity across conversations.

**Two-layer continuity:**
- An **AI summary** gives the agent high-level context from previous sessions
- The **last 10 raw messages verbatim** let it resume exactly mid-conversation — same phrasing, same decisions, same thread

## Features

- **Exact Resumption**: Last 10 raw user/assistant turns are preserved verbatim and reinjected at session start — no paraphrasing loss
- **AI-Powered Summarization**: When approaching token limits, OpenClaw generates a concise AI summary of the conversation
- **Two-Day Context**: On session start, loads today's *and* yesterday's memory so intraday context is never lost
- **Token-Safe**: Summaries capped at 6000 chars; raw messages capped at 1500 chars each — tunable
- **Seamless**: No manual intervention needed

## Installation

### Via ClawHub (recommended)

```bash
clawhub install session-context
```

### Manual

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/animo66/openclaw-skills.git tmp-skills
cp -r tmp-skills/session-context .
rm -rf tmp-skills
openclaw skills enable session-context
```

## How It Works

### Session Start Hook

When a new session begins, two context blocks are injected:

1. **AI Summary Block** — distilled summaries from today + yesterday (up to 6000 chars)
2. **Recent Messages Block** — the last 10 user/assistant turns verbatim, so the agent can resume mid-conversation without losing exact phrasing or decisions

### Compaction Hook

When token thresholds are hit (20+ messages or 60% of limit):

1. Generates an AI summary via `agent.generateSummary()`
2. Prepends it to `memory/YYYY-MM-DD.md`
3. Captures the last 10 raw message turns as a JSON block at the end of the file

### Memory File Format

```
memory/
  2026-04-03.md
  2026-04-04.md
  ...
```

Each file looks like:

```markdown
## 22:41:00
<AI summary of the session>

---

## Earlier summary...

<!-- recent_messages_block -->
[
  {"role": "user", "content": "..."},
  {"role": "assistant", "content": "..."},
  ...
]
```

The `<!-- recent_messages_block -->` marker is always at the end and replaced each compaction with the latest turns.

## Configuration

**Number of raw messages to preserve** (in both handler files):
```js
const MAX_RECENT_MESSAGES = 10;  // last N user/assistant turns
```

**Max summary context injected at session start:**
```js
const MAX_SUMMARY_CHARS = 6000;
```

**Summarization thresholds:**
```js
return (
  msgCount >= 20 ||              // minimum messages
  tokenCount > maxTokens * 0.6   // 60% of token limit
);
```

## Requirements

- OpenClaw 0.29.0 or higher
- `session:start` and `session:compact:before` hook support
- Workspace directory with `memory/` subfolder (created automatically)

## License

MIT

---

**Made with 🤖 by AniBot (Thomas)**
