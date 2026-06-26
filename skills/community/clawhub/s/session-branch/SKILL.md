---
name: "session-branch"
description: "Branch a coding session into a new conversation with full context handoff — generate structured handoff doc, startup prompts, and guide the new session to pick up exactly where you left off."
version: "1.1.0"
tags: ["session", "handoff", "branch", "context", "continuity"]
---

# Session Branch

Branch your current coding session into a new conversation without losing context.

## When to Use

- Current conversation is getting long and context compression is degrading quality
- You want to start a new task on the same project but keep full context
- You need to fork your work into a parallel direction
- User says: "开个支线" / "分叉" / "branch" / "新任务但保留上下文"

## Execution Flow

### Step 1: Analyze Current Session

Scan the current conversation and project to extract:

1. **Project identity** — name, description, platforms, version, tech stack
2. **Decision chain** — what was chosen, what was rejected, and why
3. **Data flow** — how data moves through the system (input → process → output)
4. **Capability boundary** — what the project CAN do and CANNOT do
5. **Code changes** — what files were modified in this session and why
6. **Platform status** — GitHub, ClawHub, npm, PyPI current state
7. **Environment** — which env vars are set, which need user config
8. **Knowledge files** — index of docs/knowledge/ and docs/rules/ by scenario
9. **User preferences** — language, work style, code style, security sensitivity
10. **Branchable directions** — what can be built next, with files involved and prerequisites

#### IDE-Specific Additional Scanning

**For WorkBuddy**, also scan:
- **Identity files**: `~/.workbuddy/SOUL.md`, `IDENTITY.md`, `USER.md` — persona and preferences
- **Memory files**: `.workbuddy/memory/MEMORY.md` + daily logs — project memory
- **Installed skills**: `~/.workbuddy/skills/` — list of active skills
- **Scheduled tasks**: automation/cron task list and status
- **Channel config**: IMA knowledge base IDs, Feishu channel configuration
- **MCP connectors**: active MCP connector status

**For TRAE SOLO**, also scan:
- **Rules**: `.trae/rules/` — project-level rules
- **Schedule**: TRAE SOLO Schedule task list

**For Cursor**, also scan:
- **Rules**: `.cursor/rules/` or `.cursorrules`

**For Claude Code**, also scan:
- **Rules**: `CLAUDE.md` in project root

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
- NO personal information (real names, emails, specific paths, token values)
- NO project-specific secrets or credentials
- Use generic placeholders: `<project-name>`, `<owner>`, `<your-path>`
- The handoff doc must be reusable as a TEMPLATE, not a one-time snapshot

### Step 3: Validate with Checklist

Cross-check the generated handoff against `references/checklist.md`.

Every item must be covered. If something is not applicable, write "N/A" with a reason.

### Step 4: Generate Startup Prompt

Use `references/startup-prompts.md` to generate the startup prompt for the new conversation.

The prompt must include:
1. Exact file paths for the new AI to read (absolute or relative per IDE)
2. A three-step flow: Load → Report → Ask
3. Clear role: "This is a continuation of an existing project, not starting from scratch"

### Step 5: Present to User

Show the user:
1. The generated handoff document (key sections summary)
2. The startup prompt (ready to copy-paste)
3. List of files created and their locations
4. Ask: "Ready to open a new conversation?"

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `handoff_path` | Auto (by IDE) | Where to save the handoff document |
| `include_checklist` | `true` | Whether to validate against checklist |
| `target_ide` | `auto` | Target IDE for startup prompt (auto/trae/workbuddy/cursor/claude-code) |

## References

- `references/handoff-template.md` — Full template for the handoff document
- `references/checklist.md` — Validation checklist (12 categories + IDE-specific)
- `references/startup-prompts.md` — IDE-specific startup prompt templates
