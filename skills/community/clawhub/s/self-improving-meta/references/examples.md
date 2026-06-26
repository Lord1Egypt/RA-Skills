# Entry Examples

Concrete examples of well-formatted meta entries with all fields.

## Learning: Instruction Ambiguity (Vague Delegation Threshold)

```markdown
## [LRN-20250415-001] instruction_ambiguity

**Logged**: 2025-04-15T10:30:00Z
**Priority**: high
**Status**: pending
**Area**: agent_config

### Summary
AGENTS.md says "use sub-agents for long tasks" but doesn't define "long" — causing inconsistent delegation

### Details
The delegation section in AGENTS.md states: "For long-running tasks, delegate to a sub-agent."
Different sessions interpret "long" differently — some delegate after 5 minutes of work,
others only after 10+ steps, and some never delegate at all. The instruction lacks a
concrete threshold (time-based, step-count-based, or complexity-based), resulting in
wildly inconsistent behavior across sessions.

### Suggested Action
Rewrite the delegation rule with explicit thresholds:
- "Delegate to a sub-agent when a task requires more than 8 tool calls OR
  involves modifying files in 3+ directories OR touches both frontend and backend."

Remove the vague "long-running" phrasing entirely.

### Metadata
- Source: agent_behavior_observation
- Affected Files: AGENTS.md (delegation section)
- Tags: delegation, threshold, ambiguity, agents-md
- Pattern-Key: instruction_ambiguity.vague_threshold

---
```

## Learning: Rule Conflict (Package Manager Contradiction)

```markdown
## [LRN-20250416-001] rule_conflict

**Logged**: 2025-04-16T09:00:00Z
**Priority**: high
**Status**: pending
**Area**: rule_files

### Summary
CLAUDE.md says "always use pnpm" but AGENTS.md workflow step says "npm install" — agent confused

### Details
CLAUDE.md line 42: "Package management: always use pnpm for all install and run commands."
AGENTS.md line 118 (setup workflow): "Step 3: Run `npm install` to install dependencies."

When the agent encounters the setup workflow, it faces contradictory instructions.
In 3 out of 5 sessions observed, the agent used npm (following AGENTS.md workflow order),
in 2 it used pnpm (following CLAUDE.md rule). Neither outcome was consistent.

### Suggested Action
1. Identify the authoritative source for package manager choice (CLAUDE.md for conventions)
2. Update AGENTS.md workflow step to use `pnpm install`
3. Grep all prompt files for "npm " and replace with "pnpm " where appropriate
4. Add a "Single Source of Truth" comment in AGENTS.md pointing to CLAUDE.md for tool conventions

### Metadata
- Source: agent_behavior_observation
- Affected Files: CLAUDE.md, AGENTS.md
- Tags: rule-conflict, package-manager, pnpm, npm, contradiction
- Pattern-Key: rule_conflict.package_manager

---
```

## Learning: Context Bloat (Verbose SOUL.md)

```markdown
## [LRN-20250417-001] context_bloat

**Logged**: 2025-04-17T14:00:00Z
**Priority**: medium
**Status**: pending
**Area**: prompt_files

### Summary
SOUL.md grew to 400 lines with redundant personality directives, wasting ~2K tokens per session

### Details
SOUL.md accumulated personality directives over several months without pruning:
- Lines 12-45: "Be concise and clear" expressed 6 different ways
- Lines 80-120: Communication style rules that duplicate the conciseness directives
- Lines 200-280: Historical context about the project that is now in README.md
- Lines 300-380: Deprecated workflow patterns superseded by AGENTS.md

At 400 lines, SOUL.md consumes approximately 2,000 tokens every session. After
deduplication and compression, the same behavioral guidance fits in 120 lines (~600 tokens),
saving 1,400 tokens per session for actual work context.

### Suggested Action
1. Deduplicate personality directives — one statement per behavioral rule
2. Remove content that belongs in other files (README, AGENTS.md)
3. Use structured lists instead of prose paragraphs
4. Target: SOUL.md under 150 lines, under 800 tokens

### Metadata
- Source: context_window_analysis
- Affected Files: SOUL.md
- Tags: context-bloat, soul-md, compression, token-waste
- Pattern-Key: context_bloat.verbose_soul

---
```

## Meta Issue: Hook Failure (Activator Path Changed)

```markdown
## [META-20250418-001] hook_failure

**Logged**: 2025-04-18T11:00:00Z
**Priority**: high
**Status**: pending
**Area**: hook_scripts

### Summary
activator.sh exits with code 0 but produces no output — SKILL path changed and script references old location

### Details
After reorganizing the skills directory from `./skills/` to `~/.openclaw/skills/`,
the activator.sh hook at `./skills/self-improving-meta/scripts/activator.sh` was
moved but the hook configuration in `.claude/settings.json` still points to the
old path. The shell finds no script at the old path and exits silently (code 0
because set -e doesn't trigger on a missing path in the command field).

The hook appeared to work (no errors in logs) but produced zero output for 2 weeks.
No self-improvement reminders were injected during that period.

### Root Cause
Hook configuration path was not updated after skill directory reorganization.
No validation exists to check that hook scripts actually produce output.

### Suggested Fix
1. Update hook path in `.claude/settings.json`
2. Add a health check: hook scripts should output at least a version marker
3. Consider adding a `--verify` flag to hook scripts that validates configuration
4. Log a warning if a hook produces empty output

### Metadata
- Source: hook_output_inspection
- Affected Files: .claude/settings.json, scripts/activator.sh
- Tags: hook, silent-failure, path, configuration
- Reproducible: yes

---
```

## Meta Issue: Skill Gap (Database Migration Patterns)

```markdown
## [META-20250419-001] skill_gap

**Logged**: 2025-04-19T16:00:00Z
**Priority**: medium
**Status**: pending
**Area**: skill_authoring

### Summary
No skill for database migration patterns despite 5 related learnings in .learnings/

### Details
Searching .learnings/ reveals 5 entries related to database migrations:
- LRN-20250320-003: Migration rollback failed due to missing down() method
- LRN-20250328-001: Schema change broke running queries during deployment
- LRN-20250405-002: Migration order dependency not documented
- BUG-20250410-004: Data migration corrupted timestamps due to timezone handling
- LRN-20250415-007: Idempotent migration pattern prevented duplicate column errors

These learnings share a common theme and meet extraction criteria (5 related entries,
cross-project applicability, non-obvious patterns). No skill exists to capture this
knowledge as a reusable resource.

### Suggested Fix
1. Extract a `database-migration-patterns` skill from the 5 related learnings
2. Include rollback strategy, zero-downtime patterns, idempotency
3. Update all 5 original entries with `promoted_to_skill` status

### Metadata
- Source: learnings_review
- Affected Files: .learnings/LEARNINGS.md, .learnings/BUG_PATTERNS.md
- Tags: skill-gap, database, migration, extraction-candidate
- Related Entries: LRN-20250320-003, LRN-20250328-001, LRN-20250405-002, BUG-20250410-004, LRN-20250415-007

---
```

## Feature Request: Automated Prompt File Conflict Detection

```markdown
## [FEAT-20250420-001] prompt_conflict_detector

**Logged**: 2025-04-20T10:00:00Z
**Priority**: high
**Status**: pending
**Area**: agent_config

### Requested Capability
Automated detection of contradictory instructions across AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, and copilot-instructions.md.

### User Context
Rule conflicts (like the pnpm vs npm example) go unnoticed for weeks because no tool
cross-references instructions across prompt files. Manual audits catch conflicts eventually,
but a script that flags potential contradictions at commit time or session start would
prevent agent confusion proactively.

### Complexity Estimate
medium

### Suggested Implementation
1. Parse all prompt files into structured sections (tool rules, conventions, workflows)
2. Build a keyword-to-file index (e.g., "pnpm" → CLAUDE.md:42, "npm" → AGENTS.md:118)
3. Flag entries where the same topic appears in multiple files with different instructions
4. Run as a pre-commit hook or OpenClaw bootstrap check
5. Output a conflict report with file paths and line numbers

### Metadata
- Frequency: recurring (3 conflicts found in last month)
- Related Features: prompt file linting, rule deduplication

---
```

## Learning: Promoted to AGENTS.md (Consolidated Delegation Rules)

```markdown
## [LRN-20250410-002] instruction_ambiguity

**Logged**: 2025-04-10T11:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: AGENTS.md (delegation section rewrite)
**Area**: agent_config

### Summary
Delegation rules scattered across 3 files consolidated into single authoritative section in AGENTS.md

### Details
Delegation guidance was spread across:
- AGENTS.md line 45: "Use sub-agents for complex tasks"
- SOUL.md line 88: "Prefer to handle tasks yourself unless overwhelmed"
- TOOLS.md line 23: "Sub-agent spawning is expensive, use sparingly"

These three statements gave contradictory signals. Consolidated into a single
decision table in AGENTS.md with concrete criteria, and removed delegation
mentions from SOUL.md and TOOLS.md (replaced with "See AGENTS.md for delegation policy").

### Metadata
- Source: agent_behavior_observation
- Affected Files: AGENTS.md, SOUL.md, TOOLS.md
- Tags: delegation, consolidation, single-source-of-truth
- Pattern-Key: instruction_ambiguity.scattered_delegation
- Recurrence-Count: 4
- First-Seen: 2025-03-15
- Last-Seen: 2025-04-10

---
```

## Learning: Promoted to Skill (Prompt File Compression)

```markdown
## [LRN-20250412-003] context_bloat

**Logged**: 2025-04-12T15:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/prompt-file-compression
**Area**: prompt_files

### Summary
Systematic approach to compressing verbose prompt files while preserving behavioral fidelity

### Details
Developed a repeatable compression workflow after encountering context bloat in 4 separate
prompt files over 2 months. The pattern is consistent: prompt files grow through
accretion (new rules added, old rules never removed), leading to duplication, contradiction,
and context waste.

### Compression Checklist
1. Count lines and estimate token usage
2. Identify duplicated concepts (same rule expressed differently)
3. Remove content that belongs in other files
4. Convert prose paragraphs to structured lists/tables
5. Remove historical context (move to changelog or README)
6. Verify behavioral fidelity in fresh session
7. Measure token savings

### Metadata
- Source: context_window_analysis
- Affected Files: SOUL.md, AGENTS.md, TOOLS.md, CLAUDE.md
- Tags: compression, context-bloat, prompt-engineering, token-efficiency
- See Also: LRN-20250417-001, LRN-20250325-002, LRN-20250402-004

---
```
