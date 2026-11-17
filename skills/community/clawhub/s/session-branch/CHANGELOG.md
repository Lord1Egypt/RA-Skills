# Changelog

All notable changes to session-branch will be documented in this file.

## [1.4.0] - 2026-07-15

### Security
- **Memory file reads now OPT-IN**: TRAE SOLO and WorkBuddy startup prompts require explicit user consent before reading any memory/identity files (user_profile.md, project_memory.md, topics.md, SOUL.md, MEMORY.md). Users can decline and rely on TRAE's auto-injected memory + handoff doc.
- **P0 sections now require mandatory sanitization**: "All User Messages" and "Current Work" sections must strip credentials, tokens, API keys, real names, emails, phone numbers, and personal identifiers before preserving. Replace with `<REDACTED_CREDENTIAL>` / `<REDACTED_PII>` / `<REDACTED_URL>` placeholders.
- **Removed "preserve at all costs" wording**: P0 priority now described as "preserve with mandatory sanitization" — preservation never overrides sanitization.
- **Limited User Preferences reporting**: handoff-template.md User Preferences section now records ONLY preferences that affect code generation (language, code style, workflow). Removed "Security sensitivity" field. Added explicit note: "Do NOT record personal attributes, security sensitivity levels, or any field not listed."
- **Limited memory context reporting**: TRAE SOLO and WorkBuddy startup prompts now instruct the new agent to NOT report detailed personal preferences recovered from memory files — only acknowledge "memory context recovered".

### Changed
- memory-guide.md: removed "Always read at session start" for user_profile.md and project_memory.md — changed to "Read at session start only with explicit user consent (skip if declined)"
- memory-guide.md: Quick Memory Lookup restructured as opt-in flow (ask consent → if granted, read files; if declined, rely on auto-injection only)
- startup-prompts.md TRAE SOLO: Step 4 changed to OPTIONAL opt-in with consent prompt template
- startup-prompts.md WorkBuddy: added consent gate before reading SOUL.md/MEMORY.md/IDENTITY.md/USER.md
- startup-prompts.md Customization Guide: rule 5 now requires "with user consent (OPT-IN)" for memory file reads; added rule 6 limiting what can be reported from recovered memory
- SKILL.md Permission Declaration: File read row now discloses "Reads IDE memory/identity files ONLY with explicit user consent — opt-in, never silent reads"
- SKILL.md description: added trigger boundary clarification — "Triggers ONLY on the explicit phrases '支线任务' / '开个支线' / '分叉' — do not trigger on the generic words 'branch', 'task', 'session', 'new', or 'start'"
- handoff-template.md: added Sanitization global declaration in Token Budget Allocation section

### Findings Addressed
This release addresses 10 ClawHub SkillSpector v1.3.0 audit findings:
1. Intent-Code Divergence in memory-guide.md (consent vs "always read" contradiction) — FIXED
2. Context-Inappropriate Capability — TRAE SOLO reads cross-project memory files — FIXED (opt-in)
3. Context-Inappropriate Capability — WorkBuddy reads SOUL.md/MEMORY.md — FIXED (opt-in)
4. Vague Triggers — added explicit trigger boundary in description
5. Natural-Language Policy Violations — same as Finding 1 — FIXED
6. Missing User Warnings for WorkBuddy — FIXED (consent gate added)
7. SSD3 — All User Messages preserved — FIXED (mandatory sanitization)
8. SSD3 — P0 "preserve at all costs" — FIXED (wording changed)
9. SSD3 — template reports user preferences — FIXED (field limited)
10. SSD3 — customization guide propagates privacy-invasive behavior — FIXED (consent required)

## [1.3.0] - 2026-06-12

### Added
- Trae IDE session-copy architecture fusion: 8-section fixed structure with token budget management (~4000 tokens)
- Compression strategy with P0-P3 priority levels (P0: user messages + current work; P3: conversation language)
- TRAE memory system integration: 3-layer memory reference (user profile, project memory, recent topics)
- New reference file: `references/memory-guide.md` — TRAE memory system path structure + quick lookup guide
- TRAE SOLO startup prompt enhanced: 4-layer context loading (handoff doc + rules + memory system + session_memory grep)
- All IDE startup prompts now include "unfinished Todos" reporting in Step 2
- Checklist updated with token budget verification section

### Changed
- handoff-template.md: restructured from 13 dimensions to 8 core sections + supplementary context
- checklist.md: restructured from 13 categories (A-M) to 8 core (A-H) + supplementary (I-N) + IDE-specific (O-P)
- Step 1 scanning list aligned with 8-section structure
- SKILL.md: new Step 1.5 (Apply Compression Strategy) added between scanning and document generation

## [1.2.0] - 2026-06-12

### Security
- Added Privacy & Consent section: file write warning, consent gate for IDE-specific scanning, env var value harvesting prohibition, project-relative paths only
- IDE-specific file scanning (WorkBuddy identity/memory/skills/tasks/channels/MCP) now requires explicit user consent before execution
- Environment variable scanning now records only variable names and configured status (yes/no), never values
- Fixed path contradiction: startup prompts and handoff template now use project-relative paths exclusively, never absolute paths containing usernames
- Checklist updated: added env var value check, consent verification, and absolute path prohibition

### Changed
- Trigger words updated to: "支线任务" / "开个支线" / "分叉" (removed generic "branch" and "新任务但保留上下文")
- README: added filesystem modification warning and consent notice in both Chinese and English sections

## [1.1.0] - 2026-06-04

### Added
- WorkBuddy deep adaptation: identity files (SOUL.md/IDENTITY.md/USER.md), memory system (MEMORY.md + daily logs), installed skills, scheduled tasks, IMA/Feishu channel config, MCP connectors
- IDE-specific additional scanning in SKILL.md Step 1 (WorkBuddy/TRAE SOLO/Cursor/Claude Code)
- Handoff document save location varies by IDE (`.workbuddy/` for WorkBuddy, `docs/` for others)
- Handoff template section 13: IDE-Specific Context with WorkBuddy identity/memory/skills/tasks/channels/MCP
- Checklist section M: IDE-Specific Checks (WorkBuddy 7 items, TRAE SOLO 3 items, Cursor 2 items, Claude Code 2 items)
- Branchable directions now tagged by type (Research / Engineering / Ops)
- Startup prompt for WorkBuddy now loads SOUL.md and MEMORY.md, uses `.workbuddy/session-handoff.md` path

## [1.0.0] - 2026-06-04

### Added
- Initial release
- Structured handoff document generation (12-section template)
- Validation checklist (12 categories, 40+ items)
- IDE-specific startup prompts (TRAE SOLO / WorkBuddy / Cursor / Claude Code)
- Three-step startup flow: Load → Report → Ask
- Personal information auto-filtering
- Capability boundary analysis (can/cannot/constraints)
- Branchable directions enumeration with prerequisites
