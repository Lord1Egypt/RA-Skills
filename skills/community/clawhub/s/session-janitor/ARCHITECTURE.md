# Session Janitor — Architecture & Trimming Deep Dive

## Overview

Session Janitor is a transcript hygiene system for OpenClaw gateways. It reduces context token usage by aggressively trimming JSONL session files while preserving enough history for the agent to remain coherent.

Three complementary mechanisms:
- **Sidecar (sidecar.py)** — offloads large tool outputs to `.toolcache/` files on every turn
- **Watcher (watcher.sh)** — `inotifywait` fires sidecar + trim within ~3 seconds of any turn completing
- **Cron (janitor.sh)** — runs every 15 minutes as a sweep across all sessions

---

## How Trimming Works

### What's in a Session File

Each JSONL file (`~/.openclaw*/agents/main/sessions/<uuid>.jsonl`) contains one JSON object per line:

| Type | Description |
|------|-------------|
| `session` | Header — session ID, metadata (one per file, always first) |
| `message` (user) | User message with text content |
| `message` (assistant) | Assistant response with text + tool calls |
| `message` (toolResult) | Output from tool executions |
| `compaction` | Summary stub inserted by trim or gateway compaction |

### What Gets Stripped

**Thinking blocks** (from `assistant` messages, non-recent turns):
```json
{ "type": "thinking", "thinking": "...57KB of internal reasoning...", "thinkingSignature": "..." }
```
→ Dropped entirely. The model doesn't need its old reasoning chain.

**toolCall arguments** (from `assistant` messages, non-recent turns):
```json
{ "type": "toolCall", "id": "abc123", "name": "exec", "arguments": "{\"command\":\"...long script...\"}" }
```
→ Reduced to `{ "type": "toolCall", "id": "abc123", "name": "exec" }`. The name is sufficient for context; the gateway doesn't need to re-read old arguments.

**toolResult bodies** (all but the most recent `keepFullPairs` assistant turns, default 2):
Full tool output entries (often 5-50KB each) are collapsed into a single summary line per turn:
```
exec ✓(0): first line of output | Read ✓(0) | exec ✗(1): error text
```

### What's Preserved

- **Session header** — always kept (required by gateway)
- **Last N user/assistant pairs** (default: 10, configurable via `keepPairs`) — kept verbatim. Trim fires unconditionally when over threshold — if fewer than `keepPairs` exist, all are kept.
- **Recent 2 assistant turns** — full toolResult entries preserved (configurable via `keepFullPairs`)
- **Synthetic compaction entry** — describes what was archived and why

### Two-Stage Aggressive Reduction

If the trimmed transcript still exceeds `trimFullThresholdPct`% of `trimMaxKB` (default: 50%), a second pass fires:

**Stage 1 — Strip all assistant turns:** thinking blocks and toolCall arguments dropped from every assistant entry (not just older ones).

**Stage 2 — Drop all toolResult entries:** if still over threshold after Stage 1, every `toolResult` entry is removed entirely. Only the session header, compaction stub, and raw user/assistant message text remain.

This handles sessions with very few user messages but massive tool output accumulation (e.g. stuck-loop sessions that generate hundreds of KB of tool results with only 3-4 user turns).

### Size Reduction Examples

| Session | Before | After | Reduction |
|---------|--------|-------|-----------|
| Heavy tool use + extended thinking | 401KB | 91KB | 77% |
| Normal conversation | 266KB | 100KB | 62% |
| Moderate tool use | 316KB | 102KB | 68% |
| Post-trim steady state | 157KB | 91KB | 42% |

### Token Math

Raw JSONL → tokens is roughly 4 chars/token, but JSON overhead makes it worse.

| Component | Approx tokens |
|-----------|--------------|
| System prompt + tool schemas | ~20–25k |
| Injected workspace files (SOUL, MEMORY, AGENTS, etc.) | ~5–8k |
| Total overhead before transcript | ~28–33k |
| Remaining budget (80k limit) | ~47–52k |
| 150KB trimmed transcript | ~12–15k |
| **Total at steady state** | **~40–45k / 80k** |

Before trimming, sessions routinely exceeded 80k tokens, triggering gateway compaction. After trimming, steady-state context stays around 40–45k.

---

## Sidecar Offloader

`sidecar.py` runs on every watcher-triggered write, *before* trim. It targets `toolResult` entries that exceed a size threshold (default 5KB).

### How It Works

1. Scan the JSONL for `toolResult` entries ≥ `sidecar.minEntryBytes`
2. Write the full content to `<session-id>.toolcache/<tool-call-id>.txt` (adjacent to the transcript)
3. Replace the inline content with a stub:
   ```
   [tool output offloaded to .toolcache/<tool-call-id>.txt — <N> bytes. Use the Read tool to access it if needed.]
   ```
4. If the file shrinks below the trim threshold after sidecar, skip trim entirely (and ping the gateway to reload)

### Properties

- **Idempotent** — already-stubbed entries are skipped on subsequent runs
- **Restart-safe** — `.toolcache/` files live alongside the transcript; no temp files or external state
- **Selective** — only `toolResult` entries are offloaded; user/assistant messages and thinking blocks are untouched
- **Agent-friendly** — stubs tell the agent where to find the original content if needed

### Configuration

| Key | Default | Description |
|-----|---------|-------------|
| `sidecar.enabled` | true | Enable/disable the sidecar offloader |
| `sidecar.minEntryBytes` | 5120 | Minimum toolResult content size to trigger offload |

---

## The Three Triggers

### Cron (every 15 min)

`janitor.sh` sweeps all active sessions across all gateways. Also runs:
- LLM memory extraction (extracts structured facts/decisions from archived content)
- Stale session pruning (removes orphan subagent entries)
- Archive cleanup (deletes `.pre-trim.*` files older than 7 days)

### Watcher (per-turn, ~3s latency)

`watcher.sh` uses an OS-appropriate file watcher:
- *Linux:* `inotifywait` in monitor mode (`inotify-tools` package)
- *macOS:* `fswatch` with FSEvents backend (`brew install fswatch`)

Both output one absolute path per line on write events. The rest of the flow is identical.

Flow per JSONL write event:
1. JSONL file closes after a turn completes
2. inotifywait/fswatch emits the event
3. 3-second debounce (waits for follow-on writes to finish)
4. **Run sidecar offloader** — extracts large toolResult bodies to `.toolcache/` files
5. Recheck file size — if sidecar alone brought it below threshold, skip trim and ping gateway
6. If still over threshold, verify it's an active session (check sessions.json)
7. Run `trim.py` in background
8. Ping gateway via Chat Completions API with `x-openclaw-session-key` to force in-memory reload

The reload ping is critical — without it the gateway keeps its old in-memory context until the next session load.

---

## Gateway Reload Mechanism

After trim, the watcher sends a no-op message to the gateway:

```bash
curl http://127.0.0.1:<port>/v1/chat/completions \
  -H "Authorization: Bearer <token>" \
  -H "x-openclaw-session-key: <session-key>" \
  -d '{"model":"openclaw","messages":[{"role":"user","content":"[session trimmed by maintenance — acknowledge with NO_REPLY]"}]}'
```

The `x-openclaw-session-key` header routes the request to the specific session. The gateway re-reads the JSONL file from disk before processing, so the trimmed context becomes active immediately.

The agent acknowledges with `NO_REPLY` (a special token instructing it not to send a visible reply).

---

## File Layout

```
skills/session-janitor/
├── SKILL.md                          # Agent instructions
├── ARCHITECTURE.md                   # This file
├── config.json                       # Generated by setup (gitignored)
├── config.example.json               # Reference config
├── session-janitor-watcher.service   # Systemd user service template
└── scripts/
    ├── setup.sh           # Gateway discovery, config gen, cron + service install
    ├── janitor.sh         # Cron entry point (trim + extract + prune)
    ├── trim.py            # Core transcript trimming logic
    ├── sidecar.py         # Large toolResult offloader (→ .toolcache/ files)
    ├── extract-llm.py     # LLM memory extraction from archived content
    ├── prune-sessions.py  # Stale subagent/cron session pruning
    ├── watcher.sh         # inotifywait per-turn trigger (sidecar + trim)
    ├── test-sidecar.py    # Sidecar test suite (8 scenarios, 22 assertions)
    └── test-sidecar.sh    # Shell wrapper for sidecar tests
```

### Runtime File Layout

For each session with offloaded tool outputs:
```
~/.openclaw-*/agents/main/sessions/
├── <session-id>.jsonl                # Transcript (stubs reference .toolcache/)
├── <session-id>.toolcache/            # Offloaded tool outputs
│   ├── <tool-call-id-1>.txt
│   ├── <tool-call-id-2>.txt
│   └── ...
├── <session-id>.jsonl.pre-trim.<ts>   # Pre-trim archive (if trimmed)
└── ...
```

---

## Operational Notes

- `trim.py` archives the original as `<uuid>.jsonl.pre-trim.<timestamp>` before writing
- Archives are cleaned up after 7 days (configurable via `archiveRetentionDays`)
- The watcher service restarts automatically on failure (`Restart=on-failure`)
- Watcher log: `/tmp/session-janitor-watcher.log`
- Cron log: `/tmp/session-janitor.log`
- State (dedup tracking): `~/.openclaw/session-janitor-state.json`
