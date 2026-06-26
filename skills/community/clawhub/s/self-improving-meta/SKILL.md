---
name: self-improving-meta
description: "Improves the agent infrastructure itself — core prompt files (AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md), skill definitions, hooks, rules, extensions, and memory management. Use when: (1) An agent misinterprets a prompt file instruction, (2) A hook fails or doesn't trigger, (3) A skill is not activating correctly, (4) Rules conflict across files, (5) Context window is bloated by verbose prompt files, (6) Memory entries are stale or degrading quality, (7) A skill template is missing sections or unclear."
---

# Self-Improving Meta Skill

Log infrastructure learnings, meta issues, and feature requests to markdown files for continuous improvement of the agent system itself. Captures prompt drift, rule conflicts, skill gaps, hook failures, context bloat, and instruction ambiguity. Important learnings may be promoted into the files they govern — prompt files, hook code, rule files, skill templates, and memory policies — after explicit human review.

This is the skill that improves skills. Its learnings influence infrastructure that all other skills depend on, so changes should be reviewed conservatively.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Meta Learnings\n\nPrompt drift, rule conflicts, skill gaps, hook failures, context bloat, and instruction ambiguity.\n\n**Categories**: prompt_drift | rule_conflict | skill_gap | hook_failure | context_bloat | instruction_ambiguity\n**Areas**: agent_config | skill_authoring | hook_scripts | prompt_files | rule_files | memory_management | extension_api\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/META_ISSUES.md ] || printf "# Meta Issues Log\n\nInfrastructure failures: hook crashes, skill activation problems, prompt file errors, memory corruption, extension breakage.\n\n---\n" > .learnings/META_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nCapabilities needed for agent infrastructure, skill authoring, hook development, and prompt management.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log secrets, tokens, private keys, or environment variables. Prefer short summaries or redacted excerpts over raw file contents.

Use a manual-first workflow by default. If you want reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Safety Boundaries

- Do not auto-modify core prompt files (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `MEMORY.md`) without explicit user approval.
- Prefer proposing a minimal patch and rationale before applying infrastructure changes.
- Treat hook output as sensitive; avoid logging raw command output or full transcripts.
- Keep fixes scoped to the identified issue; avoid broad refactors during incident response.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Agent misreads AGENTS.md instruction | Log to `.learnings/LEARNINGS.md` with `instruction_ambiguity` |
| Hook script fails silently | Log to `.learnings/META_ISSUES.md` |
| Skill doesn't activate when expected | Log to `.learnings/META_ISSUES.md` |
| Two rules contradict each other | Log to `.learnings/LEARNINGS.md` with `rule_conflict` |
| Prompt file too verbose, wasting context | Log to `.learnings/LEARNINGS.md` with `context_bloat` |
| Stale memory entry causes wrong behavior | Log to `.learnings/LEARNINGS.md` with `prompt_drift` |
| Skill template missing required section | Log to `.learnings/META_ISSUES.md` |
| New extension capability needed | Log to `.learnings/FEATURE_REQUESTS.md` |
| Recurring misinterpretation across sessions | Link entries, bump priority, consider promotion |
| Broadly applicable infrastructure fix | Promote directly to the affected file |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-meta
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-meta.git ~/.openclaw/skills/self-improving-meta
```

### Workspace Structure

OpenClaw injects these files into every session:

```
~/.openclaw/workspace/
├── AGENTS.md          # Multi-agent workflows, delegation patterns
├── SOUL.md            # Behavioral guidelines, personality, principles
├── TOOLS.md           # Tool capabilities, integration gotchas
├── MEMORY.md          # Long-term memory (main session only)
├── memory/            # Daily memory files
│   └── YYYY-MM-DD.md
└── .learnings/        # This skill's log files
    ├── LEARNINGS.md
    ├── META_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — prompt drift, rule conflicts, skill gaps, context bloat, instruction ambiguity
- `META_ISSUES.md` — hook crashes, skill activation failures, prompt file errors, memory corruption
- `FEATURE_REQUESTS.md` — infrastructure capabilities, tooling, automation

### Promotion Targets

When meta-learnings prove broadly applicable, promote them to the files they govern with explicit user approval:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Agent behavior corrections | `SOUL.md` | "Be concise" repeated 6 ways → single directive |
| Workflow/delegation improvements | `AGENTS.md` | Vague "long tasks" → explicit threshold |
| Tool integration fixes | `TOOLS.md` | Missing timeout guidance → add retry config |
| Memory management patterns | `MEMORY.md` | Stale entries → 30-day rotation policy |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-meta
openclaw hooks enable self-improving-meta
```

See `references/openclaw-integration.md` for complete details.

---

## Generic Setup (Other Agents)

For Claude Code, Codex, Copilot, or other agents, create `.learnings/` in the project or workspace root:

```bash
mkdir -p .learnings
```

Create the files inline using the headers shown above.

### Add reference to agent files

Add to `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`:

#### Self-Improving Meta Workflow

When agent infrastructure issues are discovered:
1. Log to `.learnings/META_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings directly to:
   - `SOUL.md` — behavioral corrections
   - `AGENTS.md` — workflow and delegation improvements
   - `TOOLS.md` — tool integration fixes
   - `MEMORY.md` — memory management policies
   - Rule files — `.cursor/rules/`, `AGENTS.md` rules
   - Hook code — fix the handler directly

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: agent_config | skill_authoring | hook_scripts | prompt_files | rule_files | memory_management | extension_api

### Summary
One-line description of the infrastructure insight

### Details
Full context: what prompt file instruction was ambiguous, which rules conflict,
why context is bloated, how memory drifted. Include the relevant file paths and
line numbers. Quote the problematic instruction verbatim.

### Suggested Action
Specific fix: rewrite the instruction, compress the file, consolidate the rules,
update the hook code, prune the memory entries.

### Metadata
- Source: agent_behavior_observation | hook_output_inspection | context_window_analysis | learnings_review | prompt_audit
- Affected Files: AGENTS.md, SOUL.md, etc.
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: rule_conflict.package_manager (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `prompt_drift` | Prompt file content no longer matches actual practices or references deleted files |
| `rule_conflict` | Two or more files give contradictory instructions on the same topic |
| `skill_gap` | No skill exists for a recurring pattern with enough learnings to extract |
| `hook_failure` | Hook script fails, produces wrong output, or doesn't trigger when expected |
| `context_bloat` | Prompt file is too verbose, duplicative, or includes stale content wasting tokens |
| `instruction_ambiguity` | Prompt file instruction is vague, causing inconsistent agent behavior |

### Meta Issue Entry [META-YYYYMMDD-XXX]

Append to `.learnings/META_ISSUES.md`:

```markdown
## [META-YYYYMMDD-XXX] issue_type

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: agent_config | skill_authoring | hook_scripts | prompt_files | rule_files | memory_management | extension_api

### Summary
Brief description of the infrastructure failure

### Error Output
\`\`\`
Actual error message, hook output, or observed misbehavior
\`\`\`

### Root Cause
What in the infrastructure caused this failure. Include the affected file and section.

### Suggested Fix
How to resolve: update hook code, fix skill frontmatter, correct prompt file, prune memory.

### Metadata
- Source: hook_output_inspection | skill_activation_failure | prompt_injection_error | memory_corruption | extension_api_breakage
- Affected Files: path/to/file
- Reproducible: yes | no | unknown
- See Also: META-20250110-001 (if recurring)

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: agent_config | skill_authoring | hook_scripts | prompt_files | rule_files | memory_management | extension_api

### Requested Capability
What infrastructure tool, automation, or capability is needed

### User Context
Why it's needed, what workflow it improves, what infrastructure problem it solves

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built: hook script, skill template, audit script, linting tool

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_feature

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `META` (meta/infrastructure issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250415-001`, `META-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is fixed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Fix Applied To**: AGENTS.md / SOUL.md / hook code / skill template
- **Notes**: Rewrote delegation instruction / compressed SOUL.md / fixed hook path
```

Other status values:
- `in_progress` — Actively investigating or fixing
- `wont_fix` — Decided not to address (add reason in Resolution notes)
- `promoted` — Elevated directly to a prompt file, rule, hook, or configuration
- `promoted_to_skill` — Extracted as a reusable meta-skill

## Promoting to Project Memory

Meta-learnings are special: they can affect shared infrastructure. When you improve a prompt file, that improvement affects future sessions. When you fix a hook, that fix can propagate to all bootstraps. Use review gates.

### When to Promote

- Same misinterpretation occurs across 2+ sessions
- Rule conflict is confirmed (not a one-off edge case)
- Context savings exceed 500 tokens after compression
- Hook failure affects multiple sessions or agents
- Skill gap has 3+ related learnings ready for extraction

### Promotion Targets

| Pattern | Action | Target |
|---------|--------|--------|
| Ambiguous instruction | Rewrite with explicit criteria | AGENTS.md / SOUL.md / TOOLS.md |
| Verbose prompt file | Compress and distill | The file itself |
| Conflicting rules | Consolidate into single authoritative source | Primary file; remove from secondary |
| Hook failure pattern | Update hook code or documentation | handler.ts/js, HOOK.md |
| Skill gap | Create new skill or update existing | New SKILL.md or existing one |
| Memory management insight | Update rotation/pruning policy | MEMORY.md |

### How to Promote

1. **Distill** the learning into a concrete fix
2. **Prepare** a minimal patch for the affected file
3. **Test** in a fresh session to verify the fix works
4. **Apply after approval**, then update original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: AGENTS.md (delegation section rewrite)` (or equivalent)

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: LRN-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring meta issues often indicate:
   - Instruction needs rewriting (→ edit the prompt file)
   - Rule belongs in a different file (→ relocate)
   - Hook needs hardening (→ add validation/output checks)
   - Skill template is incomplete (→ update template)

## Simplify & Harden Feed

Ingest recurring infrastructure patterns from `simplify-and-harden` into prompt file fixes and hook improvements.

1. For each candidate, use `pattern_key` as the dedupe key.
2. Search `.learnings/LEARNINGS.md` for existing entry: `grep -n "Pattern-Key: <key>" .learnings/LEARNINGS.md`
3. If found: increment `Recurrence-Count`, update `Last-Seen`, add `See Also` links.
4. If not found: create new `LRN-...` entry with `Source: simplify-and-harden`.

**Promotion threshold**: `Recurrence-Count >= 3`, seen in 2+ sessions, within 30-day window.

**Meta-specific actions**:
- Verbose prompt file → compress (target: 50% token reduction)
- Conflicting rules → consolidate to single source of truth
- Ambiguous instruction → rewrite with concrete examples or thresholds
- Hook producing wrong output → fix handler code and add test case

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- Before publishing a new skill
- After modifying any core prompt file (AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md)
- When adding or removing hooks
- When agent behavior degrades unexpectedly
- Monthly audit of all prompt files for staleness and conflicts

### Quick Status Check
```bash
# Count pending meta issues
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority infrastructure issues
grep -B5 "Priority\*\*: high" .learnings/META_ISSUES.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: hook_scripts" .learnings/*.md

# Find all rule conflicts
grep -B2 "rule_conflict" .learnings/LEARNINGS.md | grep "^## \["
```

### Review Actions
- Resolve fixed infrastructure issues
- Promote recurring patterns to prompt files
- Link related entries across files
- Extract skill candidates (3+ related learnings)
- Prune stale memory entries referenced in learnings

## Detection Triggers

Automatically log when you encounter:

**Instruction Problems** (→ learning with `instruction_ambiguity`):
- Agent says "I'm not sure what this instruction means" or paraphrases incorrectly
- Agent ignores a rule that should apply to the current task
- Agent asks for clarification on the same topic across multiple sessions
- Skill frontmatter description doesn't match actual behavior
- Rule file has no clear trigger condition

**Configuration Conflicts** (→ learning with `rule_conflict`):
- Two prompt files give contradictory guidance on the same topic
- CLAUDE.md convention conflicts with AGENTS.md workflow step
- .cursor/rules/ entry contradicts AGENTS.md instruction
- Skill description conflicts with global behavioral rules

**Context Issues** (→ learning with `context_bloat`):
- Agent loads too much context and truncates important information
- Prompt file exceeds 200 lines without structured formatting
- Same information duplicated across 2+ prompt files
- Historical context that belongs in README or changelog

**Memory Problems** (→ learning with `prompt_drift`):
- Memory entry references deleted files or outdated conventions
- Daily memory file contains information superseded by newer entries
- MEMORY.md rotation policy hasn't been applied in 30+ days
- Agent behavior changed because stale memory overrides current instructions

**Hook Failures** (→ meta issue):
- Hook output is empty when it shouldn't be
- Hook script exits with non-zero code
- Hook fires on wrong event or doesn't fire at expected event
- Hook configuration path points to non-existent script

**Skill Problems** (→ meta issue):
- Skill doesn't activate despite matching trigger conditions
- Skill frontmatter is malformed (missing name, description, or YAML errors)
- Skill template is missing required sections
- Skill extraction script produces invalid scaffold

## Priority Guidelines

| Priority | When to Use | Meta Examples |
|----------|-------------|---------------|
| `critical` | Agent actively doing wrong thing due to bad prompt file | Rule conflict causing harmful output, corrupted memory overriding safety rules |
| `high` | Hook failure affecting multiple sessions | Skill not activating, context bloat degrading performance, silent hook failure for 2+ weeks |
| `medium` | Instruction could be clearer | Memory needs pruning, template improvement, prompt compression opportunity |
| `low` | Documentation or style consistency | Minor template tweak, naming convention, comment formatting |

## Area Tags

Use to filter learnings by infrastructure domain:

| Area | Scope |
|------|-------|
| `agent_config` | AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, CLAUDE.md, copilot-instructions.md |
| `skill_authoring` | SKILL.md files, skill templates, skill extraction, naming conventions |
| `hook_scripts` | activator.sh, error-detector.sh, handler.ts/js, hook configuration |
| `prompt_files` | Any file injected into agent context (workspace files, rules, instructions) |
| `rule_files` | .cursor/rules/, AGENTS.md rules, coding standards files |
| `memory_management` | MEMORY.md, daily memory files, memory rotation, staleness detection |
| `extension_api` | OpenClaw extensions, tool integrations, MCP servers, ClawdHub |

## Best Practices

1. **Keep prompt files concise** — every token counts against context window
2. **One authoritative source per rule** — no duplication across files
3. **Test skills in fresh sessions** before publishing
4. **Version prompt files** — track what changed and when
5. **Audit hooks monthly** — silent failures are the worst failures
6. **Prune memory aggressively** — stale entries cause drift
7. **Write skill descriptions as trigger conditions**, not feature lists
8. **Use structured formats** (tables, lists) over prose in prompt files
9. **Quote the problematic instruction** verbatim when logging ambiguity
10. **Apply fixes directly** — meta-learnings should change the files they describe

## Hook Integration

Enable reminders through agent hooks only when needed. This is **opt-in**.

### Conservative Mode (Recommended)

- Default to **no hooks** and log manually.
- If reminders are useful, enable `UserPromptSubmit` with `scripts/activator.sh` only.
- Enable `PostToolUse` (`scripts/error-detector.sh`) only in trusted environments when you explicitly want command-output pattern checks.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-meta/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects an infrastructure-focused learning evaluation reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-meta/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-meta/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` only if you want the hook to inspect command output for infrastructure-related error terms (hook, skill, AGENTS.md, frontmatter, truncated, etc.).

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate infrastructure learnings after tasks |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on infrastructure error terms in command output |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When a meta-learning is valuable enough to become a reusable skill, extract it. Meta-skills extracting from meta-learnings is recursive improvement — the system improving itself.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same infrastructure pattern in 2+ sessions or projects |
| **Verified** | Status is `resolved` with working fix tested in fresh session |
| **Non-obvious** | Required actual investigation or multiple attempts |
| **Broadly applicable** | Not specific to one prompt file; useful across agent setups |
| **User-flagged** | User says "save this as a skill" or similar |

### Extraction Workflow

1. **Identify candidate**: Learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-meta/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-meta/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with infrastructure-specific content
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Test in fresh session**: Meta-skills require fresh session verification because they modify shared infrastructure
6. **Verify no regressions**: Ensure other skills and hooks still work

### Extraction Detection Triggers

**In conversation**: "This keeps happening", "Save this infrastructure fix as a skill", "Every project has this prompt file issue", "This hook pattern should be standard".

**In entries**: Multiple `See Also` links, high priority + resolved, `rule_conflict` or `context_bloat` with broad applicability, same `Pattern-Key` across projects.

## Meta-Improvement Loop

This skill is unique: its learnings directly modify the infrastructure that all other skills depend on. This creates a feedback loop:

1. **Observe**: Agent misinterprets instruction / hook fails / context is bloated
2. **Log**: Record the infrastructure issue in `.learnings/`
3. **Analyze**: Identify root cause (ambiguity, conflict, bloat, drift, gap, failure)
4. **Fix**: Apply correction directly to the affected file
5. **Propagate**: The fix takes effect in all future sessions for all agents
6. **Verify**: Confirm the fix works in a fresh session
7. **Learn from the fix**: If the fix itself causes issues, log that too (recursive)

When you improve a prompt file, that improvement affects all future sessions. When you fix a hook, that fix propagates to all bootstraps. When you update a skill template, all future skill extractions benefit.

The meta skill is the only skill whose learnings directly modify the infrastructure that all other skills depend on. Handle with care — test before applying.

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | Automatic via error-detector.sh |
| Codex CLI | Hooks (same pattern) | Automatic via hook scripts |
| GitHub Copilot | Manual (`.github/copilot-instructions.md`) | Manual review |
| OpenClaw | Workspace injection + inter-agent messaging | Via session tools |

## Gitignore Options

**Keep learnings local** (per-developer):
```gitignore
.learnings/
```

**Track learnings in repo** (team-wide):
Don't add to .gitignore — learnings become shared knowledge.

**Hybrid** (track templates, ignore entries):
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/meta/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: meta
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (meta)
Only trigger this skill automatically for meta orchestration signals such as:
- `cross-skill conflict|routing ambiguity|policy overlap|dedupe`
- `learning loop quality|stackability issue|prompt governance`
- explicit meta intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/meta/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
