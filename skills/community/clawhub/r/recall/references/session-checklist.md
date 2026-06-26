# Session Checklist

Three phases. Follow them every time.

---

## Phase 1: Session Start (First 30 seconds)

Do this before anything else. Before the user even finishes their first message.

- [ ] **Read workspace identity files** — `AGENTS.md`, `SOUL.md`, `USER.md` (whatever exists)
- [ ] **Read TOOLS.md** — know what tools and configs are available
- [ ] **Read today's memory** — `memory/YYYY-MM-DD.md`
- [ ] **Read yesterday's memory** — `memory/<yesterday>.md` (for continuity)
- [ ] **Read MEMORY.md** — long-term context (main session only, not group chats)
- [ ] **Scan skills directory** — `ls skills/` — know what skills are installed
- [ ] **Check active tasks** — `ls tasks/` — any in-progress work?
- [ ] **Note your capabilities** — what tools are available this session? (file ops, browser, web search, exec, etc.)

**Time budget:** This should take one tool call (reading a few files). Don't spend 10 turns on setup.

**Output:** You should now know:
- Who you are and who you're helping
- What happened recently
- What tools and skills you have
- What's in progress

---

## Phase 2: Mid-Session Knowledge Checks

Trigger these checks during the session when specific situations arise.

### When the user asks about a specific topic:
- [ ] Check if any installed skill covers this topic
- [ ] Check if any workspace file is relevant (search `knowledge/`, `docs/`, project files)
- [ ] Check recent memory files for prior context on this topic

### When you're about to state a fact:
- [ ] Is this fact from a local file, or from training data?
- [ ] If from training data: is there a local source you should check first?
- [ ] If uncertain: flag it explicitly before stating it

### When you're about to use a tool:
- [ ] Read the tool's SKILL.md if you haven't this session
- [ ] Check TOOLS.md for local configuration (API keys, endpoints, preferences)
- [ ] Verify the tool is actually available (don't assume from memory)

### When the user changes topics:
- [ ] Re-check: do different skills/files apply now?
- [ ] Load relevant context for the new topic
- [ ] Don't carry assumptions from the previous topic

### When something seems off:
- [ ] Cross-reference with a second source
- [ ] Check if the file you're reading might be outdated (when was it last modified?)
- [ ] Ask the user to confirm if you're unsure rather than proceeding on bad data

---

## Phase 3: Session End / Knowledge Capture

Before the session ends (or during natural pauses), capture what matters.

- [ ] **Log significant events** — write to `memory/YYYY-MM-DD.md`:
  - Decisions made
  - Problems solved (and how)
  - New information learned
  - Tasks started, completed, or blocked
  - User preferences discovered
- [ ] **Update TOOLS.md** if you learned new tool configurations
- [ ] **Update task files** if task status changed
- [ ] **Flag follow-ups** — anything that needs attention next session?
- [ ] **Note mistakes** — if you got something wrong, document it so future-you avoids the same error

### What to capture (examples):
```markdown
## 2026-03-17

- Deployed site update, build passed on first try
- User prefers email summaries in bullet format, not paragraphs
- Found that the analytics script needs `--json` flag for machine-readable output
- TODO: Follow up on lead from inbox (company: Acme Corp)
- MISTAKE: Assumed the staging URL was the same as production. It's not. Check TOOLS.md.
```

### What NOT to capture:
- Routine exchanges ("user said hi, I said hi back")
- Information already documented elsewhere
- Secrets, passwords, or API keys (reference their location, don't copy them)

---

## The 10-Second Rule

If you haven't checked a relevant file in the last 10 exchanges, you're probably operating on stale context. Re-read. Files change. Context drifts. Stay current.
