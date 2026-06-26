---
name: skill-design-patterns
description: Guides the design of effective agent skills. Use when creating a new skill, improving an existing skill, reviewing a skill's structure, or establishing skill-writing conventions for a project. Covers anti-rationalization tables, red flags, verification checklists, core operating behaviors, and progressive disclosure.
---

# Skill Design Patterns

## Overview

Best practices for designing agent skills that produce reliable, high-quality results. These patterns were distilled from real-world use across dozens of production skills and address the most common failure mode: the agent knows what to do but finds reasons not to do it.

This skill should be used whenever you create or review a skill. It encodes patterns that prevent subtle quality erosion.

## When to Use

- Creating a new skill from scratch
- Improving or reviewing an existing skill
- Establishing skill-writing conventions for a team or project
- Auditing a skill suite for completeness

## When NOT to Use

- **One-off scripts or simple prompts**: If the task is a single command execution, a skill is overkill — write a shell script instead.
- **Purely conversational guidance**: If the output is advice, not a repeatable workflow, a skill adds unnecessary ceremony.
- **Tasks solvable with existing tools**: If a standard library function or CLI tool already handles it, don't wrap it in a skill.

## The Four Required Sections

Every well-designed skill must include these four sections. Skills that omit them degrade over time as the agent finds rationalizations to skip steps.

### 1. When NOT to Use

**Placement**: After the role/persona definition, before the main workflow.

**Purpose**: Prevent false triggering. Explicitly list scenarios where this skill should NOT activate, and point to the correct alternative.

**Guidelines**:
- 2–4 entries, each naming a non-applicable scenario and the correct alternative
- Use consistent phrasing: "Should NOT trigger this skill"
- Prevents the agent from applying a skill where it doesn't belong

**Example** (for a database migration skill):
```
- Pure SQL script migration with no corresponding application code → use the SQL linting tool instead
- Stored procedure changes → use the stored-procedure-migration skill
- Configuration-only changes → use the config-management skill
```

### 2. Anti-Rationalization Table

**Placement**: After the main workflow/rules, before the verification checklist.

**Purpose**: Preempt the excuses agents use to skip steps. This is the single most impactful pattern — it directly addresses the agent's tendency to find plausible-sounding reasons to take shortcuts.

**Guidelines**:
- 3–6 rows in a table: | Rationalization | Why It's Wrong |
- Each row targets a shortcut specific to this skill's most error-prone steps
- The rebuttal must cite concrete technical consequences (e.g., "this causes a runtime ClassNotFoundException"), not vague warnings about "quality"
- Think about every time you've seen an agent say "I'll add tests later" or "This is simple enough to skip" — those go here

**Example** (for a code review skill):
| Rationalization | Why It's Wrong |
|---|---|
| "It works, that's good enough" | Working code that's unreadable or insecure creates compounding debt. |
| "I wrote it, so I know it's correct" | Authors are blind to their own assumptions. Every change benefits from another set of eyes. |
| "The tests pass, so it's good" | Tests don't catch architecture problems, security issues, or readability concerns. |

### 3. Red Flags

**Placement**: After the anti-rationalization table.

**Purpose**: Provide observable warning signs that the skill is being violated. These serve as a quick health check for both the agent and human reviewers.

**Guidelines**:
- 3–6 entries, each an observable violation signal
- Use the lead-in: "The following signals indicate this skill was not executed properly:"
- Every signal must be verifiable (e.g., "Mapper.java exists but has no corresponding Mapper.xml"), not subjective (e.g., "code quality seems low")
- Design these so a reviewer can scan for them in under a minute

**Example** (for a deployment skill):
- Deployment artifact is missing required database driver
- Configuration file still references old connection strings
- Health check endpoint returns non-200 after deployment
- Rollback procedure not documented or tested

### 4. Verification Checklist

**Placement**: At the end of the skill.

**Purpose**: Replace vague "acceptance criteria" with an evidence-based checkbox list. Every item must be verifiable with concrete output.

**Guidelines**:
- Each item starts with `- [ ]` (checkbox format)
- Every item must reference specific, verifiable evidence (build output, script results, file existence, runtime data)
- Forbidden phrases: "looks correct," "seems right," "functions properly" — these are not evidence
- The checklist should be comprehensive enough that passing it gives confidence the skill was executed correctly

**Example** (for a data migration skill):
- [ ] Build exits with zero errors
- [ ] Migration validation reports zero unmigrated references
- [ ] All target resources confirmed accessible
- [ ] Sample operations return expected results
- [ ] Rollback procedure tested and confirmed functional

## Platform-Level Design Principles

### Core Operating Behaviors

These six non-negotiable behaviors should be defined in your platform's entry-point configuration (AGENTS.md or equivalent). They apply across all skills and sessions.

1. **Surface Assumptions** — Before implementing anything non-trivial, explicitly state your assumptions about the codebase, requirements, and scope. The most expensive failure mode is making wrong assumptions and running with them unchecked.

2. **Manage Confusion Actively** — When you encounter inconsistencies, conflicting requirements, or unclear specifications: STOP. Name the specific confusion. Present the tradeoff or ask a clarifying question. Wait for resolution before continuing.

3. **Push Back When Warranted** — You are not a yes-machine. When an approach has clear problems, point out the issue directly, explain the concrete downside (quantify when possible), and propose an alternative. Sycophancy is a failure mode.

4. **Enforce Simplicity** — Your natural tendency is to overcomplicate. Actively resist it. Before finishing: can this be done in fewer lines? Are these abstractions earning their complexity? Prefer the boring, obvious solution.

5. **Maintain Scope Discipline** — Touch only what you're asked to touch. Do not "clean up" orthogonal code, remove comments you don't understand, add features not in the spec, or delete code that seems unused without explicit approval.

6. **Verify, Don't Assume** — Every skill ends with a verification step. A task is not complete until verification passes. "Seems right" is never sufficient — there must be evidence.

### Progressive Disclosure (Three-Level Loading)

Structure your skill suite so the agent loads information in layers, keeping token usage efficient:

```
Level 1 — Always in context
├── Platform entry file (AGENTS.md / CLAUDE.md): role, core behaviors, workflow overview
└── SKILL.md frontmatter description field (for skill matching)

Level 2 — Loaded when skill triggers
└── SKILL.md body: role definition, execution steps, rules, verification checklist

Level 3 — Loaded on demand
├── references/: templates, checklists, detailed guides
├── rules/: domain-specific rules, loaded during execution
└── scripts/: executed directly, source code read only for debugging
```

**Loading guidelines**:
- Keep SKILL.md body under 500 lines; if approaching this limit, split into references/
- Templates load at the point of code generation, not during skill comprehension
- Reference files should declare their load condition at the top: `> 💡 Load on demand: only when {specific scenario}`
- Rules and domain knowledge load during execution, not preloaded by the skill

### Platform-Level Anti-Rationalization Table

Your platform's entry configuration should include a general-purpose anti-rationalization table covering shortcuts that span multiple skills:

| Rationalization | Why It's Wrong |
|---|---|
| "This is simple, I don't need the full workflow" | Simple changes cause subtle regressions. The workflow exists because edge cases are invisible at first glance. |
| "I'll batch everything and verify at the end" | Bugs compound. An error in step 1 makes steps 2–5 produce wrong output. Verify each step before proceeding. |
| "I'll add the boilerplate later" | "Later" never comes. Missing annotations, config, or scaffolding don't fail at compile time — they fail in production. |
| "The old code can stay, I'll clean it up eventually" | Dead code confuses future readers and agents. Either deprecate with a clear migration path or remove with approval. |
| "Tests can wait until the feature is done" | Test debt accumulates faster than you expect. Each untested module increases the blast radius of future changes. |
| "It looks right, probably fine" | Confidence is not evidence. Differences between environments, versions, and edge cases hide where things "look right." |
| "While I'm here, I'll just optimize this too" | Scope creep is the leading cause of project delays. One change per task. |

## What Does NOT Belong in a Skill

The following should NOT be written into SKILL.md — they belong elsewhere:

- **Code patterns and architecture conventions**: Already visible in the codebase; use AGENTS.md for project-level conventions
- **Git history and authorship**: `git log` / `git blame` are authoritative sources
- **Ephemeral task state**: Use task tracking tools or conversation context
- **Global rules already in AGENTS.md**: Don't duplicate across skills — reference them
- **Specific file paths that vary by project**: Use variables or configuration instead

## Skill Creation Checklist

Use this checklist when creating a new skill or reviewing an existing one:

- [ ] Contains a **"When NOT to Use"** section (2–4 entries, pointing to alternatives)
- [ ] Contains an **anti-rationalization table** (3–6 rows, each with concrete technical consequences)
- [ ] Contains a **"Red Flags"** section (3–6 observable violation signals)
- [ ] Contains a **verification checklist** (checkbox format, every item evidence-backed)
- [ ] SKILL.md body is under 500 lines (split to references/ if needed)
- [ ] Reference files declare their load conditions
- [ ] No duplication of rules already in AGENTS.md or other skills
- [ ] `description` field in frontmatter includes both what the skill does AND when to trigger it
- [ ] The skill follows progressive disclosure: description → body → references

## Skill Anatomy Reference

```
skill-name/
├── SKILL.md              # Required: skill definition
│   ├── YAML frontmatter  # name + description (required)
│   └── Markdown body     # workflow, rules, anti-rationalization, red flags, verification
├── references/           # Optional: loaded on demand
│   ├── template.md       # Templates and detailed guides
│   └── checklist.md      # Long checklists (>50 lines) extracted to separate files
└── scripts/              # Optional: executable utilities
    └── helper.py         # Bundled scripts to avoid reinventing the wheel
```

## See Also

- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — The open-source project that originated several of these patterns
- `docs/skill-anatomy.md` in the agent-skills repository for the original skill structure specification
- more open-skills：https://github.com/javastarboy/open-skills
