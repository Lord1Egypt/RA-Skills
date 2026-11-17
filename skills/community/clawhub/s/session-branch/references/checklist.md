# Handoff Document Generation Checklist

When generating a handoff document, verify every item is covered.
If an item is not applicable, write "N/A" with a reason.

---

## A. Primary Request and Intent (P2, ~300 tokens)
- [ ] All user intents extracted from user messages
- [ ] Deduplicated and numbered in chronological order

## B. Key Technical Concepts (P2, ~200 tokens)
- [ ] Technical keywords extracted and deduplicated
- [ ] Categorized (Architecture / Tools / Patterns)

## C. Files and Code Sections (P1, ~1200 tokens)
- [ ] All Read/Edit/Write file operations recorded
- [ ] Each file: path + importance + change summary + key code snippet (max 500 chars)
- [ ] Project file structure overview included
- [ ] File paths are project-relative (never absolute with usernames)

## D. Errors and Fixes (P1, ~600 tokens)
- [ ] Recent 5-10 errors recorded (not all)
- [ ] Each error: description + root cause + fix solution

## E. Problem Solving (P2, ~300 tokens)
- [ ] Completed achievements summarized
- [ ] Key decisions documented (chosen vs rejected + reason)

## F. All User Messages (P0, ~800 tokens)
- [ ] All user messages preserved as original text **with mandatory sanitization**
- [ ] Credentials, tokens, API keys, passwords replaced with `<REDACTED_CREDENTIAL>`
- [ ] Real names, emails, phone numbers replaced with `<REDACTED_PII>`
- [ ] Absolute paths with usernames converted to project-relative paths
- [ ] Messages >500 chars truncated with "..."

## G. Conversation Language (P3, ~10 tokens)
- [ ] Primary conversation language detected and recorded

## H. Current Work (P0, ~600 tokens)
- [ ] Active task described (what is being worked on right now)
- [ ] Unfinished Todos listed with status and files involved
- [ ] Branchable directions listed with type, files, prerequisites, complexity

---

## Supplementary: Project Context

### I. Project Identity
- [ ] Project name, description, platforms, version, tech stack, license
- [ ] Project directory is relative path (never absolute)

### J. Platform Status
- [ ] GitHub repo + release status
- [ ] ClawHub version + security status (if applicable)

### K. Environment Variables
- [ ] Env var names listed (yes/no status only)
- [ ] Which need user configuration
- [ ] Token types and required permissions
- [ ] No env var values recorded anywhere

### L. Capability Boundary
- [ ] What the project CAN do
- [ ] What the project CANNOT do
- [ ] Dependency constraints

### M. Knowledge File Index
- [ ] Indexed by scenario (not by filename)
- [ ] Priority annotated (Must-read / On-demand)

### N. User Preferences
- [ ] Preferred language, code style, workflow preferences recorded
- [ ] Only preferences affecting code generation recorded (no personal attributes, no security sensitivity)

---

## O. Startup Prompt
- [ ] Three-step flow: Load -> Report -> Ask
- [ ] Adapted for target IDE platform
- [ ] Role set: "continuation of existing project, not starting from scratch"
- [ ] Project-relative file paths (never absolute with usernames)
- [ ] For TRAE SOLO: memory system reads are OPT-IN with explicit consent prompt
- [ ] For WorkBuddy: identity/memory file reads are OPT-IN with explicit consent prompt
- [ ] Memory context reporting limited to project conventions + recent topics (no detailed personal preferences)

---

## P. IDE-Specific Checks (fill based on target IDE)

### For TRAE SOLO
- [ ] Memory system reference included (user_profile, project_memory, recent topics)
- [ ] Explicit user consent obtained before reading any memory files
- [ ] `.trae/rules/` indexed
- [ ] Schedule tasks listed
- [ ] Handoff saved to `docs/session-handoff.md`

### For WorkBuddy
- [ ] Identity files indexed (SOUL.md, IDENTITY.md, USER.md)
- [ ] Memory system indexed (MEMORY.md, daily logs)
- [ ] Explicit user consent obtained before reading identity/memory files
- [ ] Installed skills listed
- [ ] Scheduled tasks (automations) listed with status
- [ ] MCP connector status documented
- [ ] Handoff saved to `.workbuddy/session-handoff.md`

### For Cursor
- [ ] `.cursor/rules/` or `.cursorrules` indexed
- [ ] Handoff saved to `docs/session-handoff.md`

### For Claude Code
- [ ] `CLAUDE.md` indexed
- [ ] Handoff saved to `docs/session-handoff.md`

---

## Personal Information Filter

Before finalizing the handoff, scan and remove:

- [ ] No real names (use `<owner>` or `<contributor>`)
- [ ] No real email addresses
- [ ] No absolute paths containing usernames (use `<project-dir>`)
- [ ] No token values (use `<your-token>`)
- [ ] No env var values (only variable names + configured status)
- [ ] No internal network addresses or VPN endpoints
- [ ] No project-specific secrets or API keys
- [ ] No personal preferences that are project-specific (keep generic patterns)
- [ ] IDE-specific file scanning was performed with explicit user consent

---

## Token Budget Verification

- [ ] Total handoff doc is approximately 4000 tokens (8 core sections)
- [ ] P0 sections (All User Messages + Current Work) have the most detail
- [ ] P3 sections (Conversation Language) are minimal
- [ ] Supplementary sections are NOT counted toward the 4000-token budget
