---
name: "session-branch"
description: "Branch a coding session into a new conversation with full context handoff — generate structured handoff doc and startup prompts. Triggers ONLY on '支线任务' / '开个支线' / '分叉'. Do NOT use for new projects, general coding, or non-handoff session management."
version: "1.4.0"
slug: "session-branch"
displayName: "Session Branch"
summary: "将当前编码会话分叉到新对话，完整保留上下文。自动生成结构化交接文档和启动提示词。"
license: "MIT-0"
tags: ["session", "handoff", "branch", "context", "continuity"]
---

# Session Branch

Branch your current coding session into a new conversation without losing context.

## When to Use

- Current conversation is getting long and context compression is degrading quality
- You want to start a new task on the same project but keep full context
- You need to fork your work into a parallel direction
- User says: "支线任务" / "开个支线" / "分叉"

## Privacy & Consent

**Before executing any step, the agent MUST:**

1. **Warn the user** that this skill will write a file to the project directory (e.g., `docs/session-handoff.md`)
2. **Ask for explicit consent** before scanning any IDE-specific identity, memory, or configuration files
3. **Never harvest env var values** — only record variable names and whether they are configured (yes/no)
4. **Use project-relative paths** in all generated documents — never absolute paths containing usernames or home directories

## Execution Flow

### Step 1: Analyze Current Session

Scan the current conversation and project to extract:

1. **Primary request and intent** — all user intents, deduplicated, numbered chronologically
2. **Key technical concepts** — keywords, categorized (Architecture / Tools / Patterns)
3. **Files and code sections** — all Read/Edit/Write operations, with change summaries and key snippets
4. **Errors and fixes** — recent 5-10 errors with root cause and solution
5. **Problem solving** — completed achievements + key decision chain (chosen vs rejected + why)
6. **All user messages** — original text preserved **with sanitization** (strip credentials/PII), truncate >500 chars with "..."
7. **Conversation language** — detected primary language
8. **Current work** — active task, unfinished Todos with status, branchable directions

**Supplementary context** (not token-budgeted): project identity, platform status, env var names (status only), capability boundary, knowledge file index, user preferences.

#### IDE-Specific Additional Scanning

> **Consent required**: Before scanning any of the following, inform the user what files will be accessed and ask for explicit permission. Skip any category the user declines.

**For WorkBuddy**, also scan (with user consent):
- **Identity files**: `~/.workbuddy/SOUL.md`, `IDENTITY.md`, `USER.md` — persona and preferences
- **Memory files**: `.workbuddy/memory/MEMORY.md` + daily logs — project memory
- **Installed skills**: `~/.workbuddy/skills/` — list of active skills
- **Scheduled tasks**: automation/cron task list and status
- **Channel config**: IMA knowledge base IDs, Feishu channel configuration
- **MCP connectors**: active MCP connector status

**For TRAE SOLO**, also scan (with user consent):
- **Rules**: `.trae/rules/` — project-level rules
- **Schedule**: TRAE SOLO Schedule task list
- **Memory system**: `~/.trae-cn/memory/` — user profile, project memory, recent topics (see `references/memory-guide.md` for path structure)

**For Cursor**, also scan:
- **Rules**: `.cursor/rules/` or `.cursorrules`

**For Claude Code**, also scan:
- **Rules**: `CLAUDE.md` in project root

### Step 1.5: Apply Compression Strategy

> Based on Trae IDE session-copy architecture. The handoff doc uses an 8-section fixed structure with token budget management.

**8 Core Sections** (token budget ~4000 total):

| # | Section | Priority | Budget | Rule |
|---|---------|----------|--------|------|
| 1 | Primary Request and Intent | P2 | ~300 | Numbered list, deduplicated |
| 2 | Key Technical Concepts | P2 | ~200 | Keyword list, categorized |
| 3 | Files and Code Sections | P1 | ~1200 | Paths + changes + snippets (max 500 chars each) |
| 4 | Errors and Fixes | P1 | ~600 | Recent 5-10 only, description + cause + fix |
| 5 | Problem Solving | P2 | ~300 | Completed achievements + decision chain |
| 6 | All User Messages | P0 | ~800 | Original text **with sanitization** (strip credentials/PII), truncate >500 chars with "..." |
| 7 | Conversation Language | P3 | ~10 | Single field |
| 8 | Current Work | P0 | ~600 | Active task + unfinished Todos + branchable directions **with sanitization** (no personal paths) |

**Compression priority**: When content exceeds budget, compress in reverse priority order (P3 first, P0 last):
- **P3** (can discard): Conversation Language is just one word
- **P2** (summary only): Compress to keyword lists
- **P1** (keep recent): Only recent 5-10 errors, only key code snippets
- **P0** (preserve **with mandatory sanitization**): All user messages and current work status — strip credentials, tokens, real names, emails, and personal identifiers before preserving; replace with `<REDACTED>` placeholders

**Supplementary sections** (not budgeted): Project identity, platform status, env vars, capability boundary, knowledge index, user preferences, IDE-specific context (with consent).

### Step 2: Generate Handoff Document

Use the template at `references/handoff-template.md` to create a structured handoff document.

**Save location by IDE**:

| IDE | Default path | Rationale |
|-----|-------------|-----------|
| WorkBuddy | `.workbuddy/session-handoff.md` | Align with memory system, keep project root clean |
| TRAE SOLO | `docs/session-handoff.md` | Standard docs location |
| Cursor | `docs/session-handoff.md` | Standard docs location |
| Claude Code | `docs/session-handoff.md` | Standard docs location |

**Critical rules**:
- NO personal information (real names, emails, token values)
- NO project-specific secrets or credentials
- Use project-relative paths (e.g., `docs/session-handoff.md`), never absolute paths containing usernames or home directories
- Use generic placeholders: `<project-name>`, `<owner>`, `<your-path>`
- The handoff doc must be reusable as a TEMPLATE, not a one-time snapshot

### Step 3: Validate with Checklist

Cross-check the generated handoff against `references/checklist.md`.

Every item must be covered. If something is not applicable, write "N/A" with a reason.

### Step 4: Generate Startup Prompt

Use `references/startup-prompts.md` to generate the startup prompt for the new conversation.

The prompt must include:
1. Project-relative file paths for the new AI to read (never absolute paths with usernames)
2. A three-step flow: Load → Report → Ask
3. Clear role: "This is a continuation of an existing project, not starting from scratch"

### Step 5: Present to User

Show the user:
1. The generated handoff document (key sections summary)
2. The startup prompt (ready to copy-paste)
3. List of files created and their locations
4. Ask: "Ready to open a new conversation?"

## Permission Declaration

| Capability | Used | Description |
|------------|------|-------------|
| Network | No | No network access required |
| File read/write | Yes | Reads project files; writes `docs/session-handoff.md` (overwrites if exists). Reads IDE memory/identity files (e.g., `~/.trae-cn/memory/`, `~/.workbuddy/SOUL.md`) **ONLY with explicit user consent** — opt-in, never silent reads |
| Environment variables | Yes | Reads env var names (status only, never values) |
| subprocess | No | No subprocess calls |
| External API | No | No external API calls |

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `handoff_path` | Auto (by IDE) | Where to save the handoff document |
| `include_checklist` | `true` | Whether to validate against checklist |
| `target_ide` | `auto` | Target IDE for startup prompt (auto/trae/workbuddy/cursor/claude-code) |

## References

- `references/handoff-template.md` — Full template for the handoff document (8 sections + supplementary context)
- `references/checklist.md` — Validation checklist (8 core sections + supplementary + IDE-specific)
- `references/startup-prompts.md` — IDE-specific startup prompt templates (5 IDEs with memory integration)
- `references/memory-guide.md` — TRAE memory system reference (3 layers + quick lookup guide)
