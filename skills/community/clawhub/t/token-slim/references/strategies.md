# Token Saving Strategies — Reference

## The Core Problem

Every message sent to an LLM includes: system prompt + project context files + conversation history + current message. All of this costs tokens. The larger and messier these files, the more tokens burned every single turn — even on trivial questions.

Output tokens cost 4–8× more than input tokens. Verbose replies are expensive.

---

## Strategy 1: Memory File Hierarchy (分层记忆)

Split memory into tiers, load only what's needed:

| Tier | File | When Loaded | Size Target |
|------|------|-------------|-------------|
| Always-on | MEMORY.md | Every session | < 150 lines |
| On-demand | memoryres/*.md | When topic comes up | Unlimited |
| Raw log | memory/YYYY-MM-DD.md | Rarely | Unlimited |

**Rule**: MEMORY.md should contain pointers and essentials only. Move anything that's read < once a week to `memoryres/`.

**Signs a section belongs in memoryres/**:
- It's a reference table (vocab, OKR, tech specs)
- It hasn't been mentioned in the last 5 conversations
- It's > 30 lines and self-contained
- It's a "someday" item (pending tasks, migration backlog)

---

## Strategy 2: System Prompt / Project Context Trim

Files injected into every session (MEMORY.md, AGENTS.md, SOUL.md, USER.md, etc.) burn tokens on every single message.

**Audit questions for each file:**
- Is every section genuinely needed every session?
- Can any section be replaced with a `→ See memoryres/xxx.md` pointer?
- Are there long tables, code blocks, or examples that are rarely referenced?

**Common wins:**
- OKR tables → `memoryres/okr.md`
- Vocabulary / glossary → `memoryres/vocab.md`
- Tech migration backlogs → `memoryres/tech-debt.md`
- CSS/code references → `memoryres/code-refs.md`
- Historical incident notes → `memoryres/incidents.md`

---

## Strategy 3: Session Boundary Discipline

A long conversation accumulates context that never gets cleaned up. Each turn re-sends the entire history.

**Rules:**
- Start a new session when a topic clearly ends
- After 20 turns, proactively suggest `/new`
- After completing a multi-step task, summarize key decisions into `memory/YYYY-MM-DD.md` before switching sessions

**Compaction vs. /new:**
- Compaction: OpenClaw auto-compresses history when context approaches limit (reactive)
- `/new`: User-initiated fresh session (proactive, better control)

Prefer proactive `/new` over waiting for compaction failures.

---

## Strategy 4: HEARTBEAT.md Budget Control

HEARTBEAT.md is loaded on every heartbeat poll. Keep it surgical:

- **Target**: < 50 lines
- **Remove**: Completed tasks, stale reminders, resolved incidents
- **Keep**: Active recurring checks, pending retries, launch checklist items
- **Anti-pattern**: Long explanatory prose in HEARTBEAT.md (move to AGENTS.md or memoryres/)

---

## Strategy 5: Subagent Isolation

Long tasks (scraping, batch processing, multi-step analysis) pollute the main session context with tool call results and intermediate outputs.

**Rule**: Tasks estimated > 30 seconds → use `sessions_spawn`.

Benefits:
- Main session stays clean
- Parallel execution
- Results delivered as a summary, not a wall of tool outputs

---

## Strategy 6: Silent Reply Discipline

Every response has a token cost. Unnecessary responses (heartbeat ACKs, "noted", "understood") add up.

**Apply:**
- Heartbeat with nothing to do → `HEARTBEAT_OK` only
- Group chat with no value to add → `NO_REPLY`
- Routine tool calls → no narration unless it helps

---

## Strategy 7: Output Brevity

Output tokens are 4–8× more expensive than input tokens.

**Practices:**
- Skip "Great question!" and similar filler
- Use bullet lists over paragraphs for reference info
- For confirmations, one sentence is enough
- For status updates, lead with the result, then details

---

## Scoring Rubric (for scan analysis)

When scanning a workspace, score each item:

| Issue | Severity | Token Impact |
|-------|----------|-------------|
| MEMORY.md > 200 lines | High | ~2k tokens/session |
| Tables/code blocks in always-on files | High | 500-2k tokens/section |
| HEARTBEAT.md > 60 lines | Medium | 300-600 tokens/heartbeat |
| No session boundary habit | Medium | Accumulates over time |
| Verbose heartbeat responses | Medium | 100-500 tokens/heartbeat |
| No subagent usage for long tasks | Low | Context bloat |
| Repeated filler in replies | Low | Output token waste |
