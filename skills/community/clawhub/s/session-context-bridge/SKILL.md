# Session Context Bridge

> Never start from zero. Carry context across sessions automatically.

## The Problem

Every new session starts blind. You lose:
- What you were working on yesterday
- Decisions made and why
- Unfinished tasks and their state
- Environment details (paths, configs, credentials setup)
- Relationships between files and projects

Claude-mem (65K stars) proved this is a massive need. This is the lightweight, framework-agnostic version.

## When to Use

- "save my context", "restore session", "continue from yesterday"
- End of every working session
- Start of every new session
- Before context-switching between projects

## How It Works

### End of Session: Save
```markdown
## Session Context — 2026-04-22 03:00

### Active Task
- Building API endpoint for user onboarding
- Status: 70% complete, auth middleware done, tests pending

### Key Decisions
1. Chose JWT over session cookies (reason: mobile-first, stateless)
2. Rate limiting: 100 req/min per user
3. Database: PostgreSQL with UUID primary keys

### File Map
- `src/auth/middleware.ts` — JWT validation (DONE)
- `src/routes/onboarding.ts` — Main endpoint (IN PROGRESS, line 47)
- `tests/onboarding.test.ts` — Not started
- `prisma/schema.prisma` — User model updated

### Blockers
- Waiting on design team for email template
- Need staging database credentials from DevOps

### Environment
- Node v22.22.2, pnpm 10.28
- DATABASE_URL in .env (not committed)
- Redis running on localhost:6379
```

### Start of Session: Restore
```markdown
## Restoring Context from 2026-04-22 03:00

### Resume Point
→ Continue `src/routes/onboarding.ts` at line 47
→ Next: implement email verification flow
→ Then: write tests

### Context Loaded
- 3 key decisions loaded
- File map: 4 files
- 2 blockers noted
- Environment confirmed

Ready to continue.
```

## Context File Structure

```
project/
├── .context/
│   ├── current.md        ← Active session context (always up-to-date)
│   ├── archive/
│   │   ├── 2026-04-20.md ← Previous sessions
│   │   └── 2026-04-21.md
│   └── decisions.md      ← Long-running decision log
```

### `current.md` Template

```markdown
# Session Context

> Last updated: [TIMESTAMP]

## 🎯 Active Task
[What you're working on right now]

## ✅ Completed This Session
- [x] Task 1
- [x] Task 2

## 🔄 In Progress
- [ ] Task 3 (status: ___)

## 📋 Todo (Next Session)
- [ ] Task 4
- [ ] Task 5

## 🧠 Key Decisions
1. [Decision] — [Reason]

## 📁 File Map
| File | Status | Notes |
|------|--------|-------|
| path/to/file | DONE/WIP/TODO | Description |

## 🚧 Blockers
- [What's blocking you]

## 🔧 Environment
- Runtime versions
- Active services
- Config state
```

### `decisions.md` Template

```markdown
# Decision Log

> Architectural and design decisions with reasoning.

## [DATE] — [Decision Title]
- **Decision:** [What was decided]
- **Context:** [What was the situation]
- **Reason:** [Why this option was chosen]
- **Alternatives:** [What else was considered]
- **Revisit if:** [Conditions that might change this decision]
```

## Bridge Protocol

### Save (End of Session)
1. Write `current.md` with all sections filled
2. Copy to `archive/YYYY-MM-DD.md`
3. Update `decisions.md` with any new decisions
4. Verify file written: `cat .context/current.md | head -5`

### Restore (Start of Session)
1. Read `.context/current.md`
2. Read `.context/decisions.md`
3. Verify environment matches (runtime versions, services)
4. Check file map: `git status` vs expected state
5. Resume from "In Progress" section

### Context Switch (Between Projects)
1. Save current project context
2. Load target project context
3. Note: different `.context/` directories per project

## Anti-Patterns

- ❌ Writing novels — context should be scannable in 30 seconds
- ❌ Including raw output — summarize, don't copy-paste
- ❌ Forgetting environment state — "works on my machine" starts here
- ❌ Only saving when done — in-progress state is MORE valuable
- ❌ Not archiving — `current.md` becomes useless without history

## Integration with Existing Tools

- **OpenClaw:** Context files auto-loaded via workspace
- **Claude Code:** Use as CLAUDE.md supplementary context
- **Cursor:** Map to `.cursor/rules/context.mdc`
- **Generic:** Works with any agent that can read files

## License

MIT
