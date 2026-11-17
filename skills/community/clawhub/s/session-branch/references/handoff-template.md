# Session Handoff Document Template

> This template defines the structure for a project handoff document.
> Based on Trae IDE session-copy architecture: 8 fixed sections with token budget management.
> **Never include personal information** — use placeholders for names, paths, and credentials.

---

## Token Budget Allocation

> Total target: ~4000 tokens. Use the priority table below to compress when content exceeds budget.
>
> **Sanitization applies to ALL sections (including P0)**: Before preserving any user content, strip credentials, tokens, API keys, real names, emails, phone numbers, and personal identifiers. Replace with `<REDACTED>` placeholders. Preservation priority never overrides sanitization — sensitive content is always redacted, even in P0 sections.

| Priority | Section | Token Budget | Compression Rule |
|----------|---------|-------------|-----------------|
| **P0** | All User Messages | ~800 | Preserve original text **with sanitization** (strip credentials/PII, replace with `<REDACTED>`); truncate messages >500 chars with "..." |
| **P0** | Current Work | ~600 | Detailed description of current task state + unfinished Todos **with sanitization** (no token values, no personal paths) |
| **P1** | Files and Code Sections | ~1200 | File paths + modification summary + key code snippets (max 500 chars each) |
| **P1** | Errors and Fixes | ~600 | Error description + solution; keep only recent 5-10 items |
| **P2** | Primary Request and Intent | ~300 | Numbered list, deduplicated |
| **P2** | Key Technical Concepts | ~200 | Keyword list, deduplicated and categorized |
| **P2** | Problem Solving | ~300 | Summary of completed achievements |
| **P3** | Conversation Language | ~10 | Single field |

---

## 1. Primary Request and Intent

> P2 priority | ~300 tokens | Extract from all user messages, deduplicate, number in chronological order

1. `<intent-1>`
2. `<intent-2>`
3. `<intent-3>`

---

## 2. Key Technical Concepts

> P2 priority | ~200 tokens | Extract technical keywords, deduplicate, categorize

- **Architecture**: `<concepts>`
- **Tools/Libraries**: `<concepts>`
- **Patterns**: `<concepts>`

---

## 3. Files and Code Sections

> P1 priority | ~1200 tokens | Record all Read/Edit/Write operations. Keep file path + modification summary + key code snippet (max 500 chars)

| File | Importance | Changes | Key Code Snippet |
|------|-----------|---------|-----------------|
| `<file-1>` | `<why-it-matters>` | `<what-changed>` | `<snippet or "see file">` |
| `<file-2>` | `<why-it-matters>` | `<what-changed>` | `<snippet or "see file">` |

**Project file structure overview**:
```
<project-name>/
├── <file-1>                  # <description>
├── <dir-1>/
│   └── <file>                # <description>
└── <dir-2>/
    └── <file>                # <description>
```

---

## 4. Errors and Fixes

> P1 priority | ~600 tokens | Keep only recent 5-10 errors. Record error description + root cause + solution

| # | Error | Root Cause | Fix |
|---|-------|-----------|-----|
| 1 | `<error-description>` | `<cause>` | `<solution>` |
| 2 | `<error-description>` | `<cause>` | `<solution>` |

---

## 5. Problem Solving (Completed Achievements)

> P2 priority | ~300 tokens | Summary of what was accomplished

- ✅ `<achievement-1>`
- ✅ `<achievement-2>`

**Decision chain** (key choices made and why):

| Decision | Chosen | Rejected | Reason |
|----------|--------|----------|--------|
| `<decision>` | `<chosen>` | `<alt>` | `<why>` |

---

## 6. All User Messages

> P0 priority | ~800 tokens | Preserve original text **with mandatory sanitization**. Truncate messages >500 chars with "..."

**Sanitization checklist (apply to each message before preserving):**
- Replace credentials, tokens, API keys, passwords → `<REDACTED_CREDENTIAL>`
- Replace real names, emails, phone numbers → `<REDACTED_PII>`
- Replace absolute paths containing usernames → project-relative paths
- Replace personal identifiers in URLs → `<REDACTED_URL>`

1. `<sanitized-user-message-1>`
2. `<sanitized-user-message-2>`
3. `<sanitized-user-message-3>`
4. "..."

---

## 7. Conversation Language

> P3 priority | ~10 tokens

`<language>`

---

## 8. Current Work

> P0 priority | ~600 tokens | Describe current task state, unfinished Todos, and next steps

### Active Task
`<what-is-being-worked-on-right-now>`

### Unfinished Todos
| # | Task | Status | Files Involved |
|---|------|--------|---------------|
| 1 | `<task>` | in_progress | `<files>` |
| 2 | `<task>` | pending | `<files>` |

### Branchable Directions
| # | Direction | Type | Files | Prerequisites | Complexity |
|---|-----------|------|-------|---------------|-----------|
| A | `<direction>` | Research/Eng/Ops | `<files>` | `<prereqs>` | Low/Med/High |
| B | `<direction>` | Research/Eng/Ops | `<files>` | `<prereqs>` | Low/Med/High |

---

## Supplementary: Project Context

> Include these sections below the 8 core sections. They provide context but are NOT part of the token-budgeted summary.

### Project Identity

| Field | Value |
|-------|-------|
| Project name | `<project-name>` |
| Description | `<one-line>` |
| GitHub | `https://github.com/<owner>/<repo>` |
| ClawHub slug | `<slug>` (if applicable) |
| Current version | `<X.Y.Z>` |
| Project directory | `<project-dir>` (relative path only) |
| Tech stack | `<language> / <framework> / <tools>` |
| License | `<license-type>` |

### Platform Status

| Platform | Version | Status |
|----------|---------|--------|
| GitHub | `<version>` | `<release-status>` |
| ClawHub | `<version>` | `<security-status>` |

### Environment Variables

> **Never record env var values.** Only list variable names and whether they are configured.

| Variable | Purpose | Status |
|----------|---------|--------|
| `<VAR_1>` | `<purpose>` | Configured / Needs user config |

### Capability Boundary

**Can Do**: `<capabilities>`
**Cannot Do**: `<limitations>`
**Dependencies**: `<constraints>`

### Knowledge File Index

| Need | File to Read | Priority |
|------|-------------|----------|
| `<scenario>` | `<path>` | Must-read / On-demand |

### User Preferences

> Record ONLY preferences that directly affect code generation. Do NOT record personal attributes, security sensitivity levels, or any field not listed below.

| Preference | Value |
|-----------|-------|
| Preferred language | `<language>` |
| Code style | `<style>` |
| Workflow preferences | `<style>` |

---

## Startup Prompt for New Session

(Generated from `references/startup-prompts.md` based on target IDE)

---

## IDE-Specific Context (Optional — fill based on target IDE)

> **Consent required**: Only fill this section after obtaining explicit user consent to scan these files.

### For TRAE SOLO

#### Memory System Reference

> The new session's agent should read these files to recover cross-session memory. See `references/memory-guide.md` for full details.
> **Consent required**: The agent should inform the user before reading memory files, as they may contain personal preferences and project-internal information.

| Memory Layer | Path | Purpose |
|-------------|------|---------|
| User profile | `~/.trae-cn/memory/user_profile.md` | Cross-project user preferences |
| Project memory | `~/.trae-cn/memory/projects/<project-key>/project_memory.md` | Project conventions + lessons |
| Recent topics | `~/.trae-cn/memory/projects/<project-key>/<YYYYMMDD>/topics.md` | Recent session topic summaries |

> **Note**: TRAE auto-injects memory context via `<memory_item>` tags in system reminders. The new session's agent should still be told to check these files explicitly, as auto-injection may not cover all relevant entries.

#### Rules
| File | Path | Description |
|------|------|-------------|
| Project rules | `.trae/rules/` | Auto-loaded project rules |

#### Scheduled Tasks
| Task | Cron | Status |
|------|------|--------|
| `<task>` | `<cron>` | Active/Paused |

### For WorkBuddy

#### Identity Files
| File | Path | Description |
|------|------|-------------|
| SOUL.md | `~/.workbuddy/SOUL.md` | Persona definition |
| IDENTITY.md | `~/.workbuddy/IDENTITY.md` | Identity configuration |
| USER.md | `~/.workbuddy/USER.md` | User profile |

#### Memory System
| File | Path | Description |
|------|------|-------------|
| Project memory | `.workbuddy/memory/MEMORY.md` | Project-level memory |
| Daily logs | `.workbuddy/memory/YYYY-MM-DD.md` | Daily session logs |

#### Installed Skills
| Skill | Version | Status |
|-------|---------|--------|
| `<skill>` | `<version>` | Active |

#### Scheduled Tasks
| Task | Cron | Status |
|------|------|--------|
| `<task>` | `<cron>` | Active/Paused |

#### MCP Connectors
| Connector | Status |
|-----------|--------|
| `<connector>` | Connected/Disconnected |

### For Cursor

| File | Path | Description |
|------|------|-------------|
| Project rules | `.cursor/rules/` or `.cursorrules` | Auto-loaded project rules |

### For Claude Code

| File | Path | Description |
|------|------|-------------|
| Project rules | `CLAUDE.md` | Project-level instructions |
