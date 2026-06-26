# SKILL-STANDARD.md — OpenClaw Skill Quality Standard

> Version: 1.0.0
> Based on Claude Code source code analysis
> Core references: Anthropic official SKILL documentation + industry best practices

---

## Core Principles

### 1. Description is the Only Trigger

OpenClaw triggers a skill based only on the `description` field in YAML frontmatter. Body content loads only after triggering.

**Description must be "strong enough" — make the model immediately recognize "this is the skill's job, not the general agent's job."**

```yaml
# Correct: Strong enough, model knows to trigger
description: "Use when user says 'search', 'look up', '帮我查', '搜一下', 'find information' for real-time web information"

# Wrong: Too vague, model won't trigger
description: "Tavily API search tool for information retrieval"
```

### 2. Three-Layer Progressive Disclosure

Information loads in three layers:

```
Layer 1 -- Metadata (~100 tokens) -- Always loaded at startup
Layer 2 -- SKILL.md body (~2,000 tokens) -- Loaded on skill trigger
Layer 3 -- references/scripts/assets -- Loaded on demand
```

**Design Principles:**
- SKILL.md body < 500 lines; detailed content in `references/`
- Scripts do not go into context, only execution results
- 20 skills at startup only use ~2,000 tokens, not ~40,000

### 3. Static/Dynamic Separation

| Static (in SKILL.md) | Dynamic (runtime) |
|---------------------|-------------------|
| Identity, tool specs, safety constraints | `!command` output, user input |
| Description triggers | git state, runtime variables |
| references/ paths (not content) | Context-generated script output |

### 4. Self-Awareness of Ignorance

**Stay silent on what you do not know.**

Do not speculate or fabricate details about:
- API request/response JSON structures not verified
- Internal implementation of external systems
- Command syntax for tools outside your knowledge
- Configuration formats you cannot confirm

When in doubt, omit or flag as unverified.

---

## Six Dimensions

| Dimension | Required | Description |
|-----------|----------|-------------|
| Metadata | Yes | name + **description** is core |
| Lean body | Yes | < 500 lines; detailed content in references/ |
| STATIC section | Yes | Identity + tool specs + safety constraints |
| Dynamic section | Suggested | Use `!command` or {$VAR} |
| Execution flow | Yes | Branches + [Prepare/Execute/Verify/Report] |
| Output specification | Yes | Success + failure JSON |

---

## Grade Rating

| Grade | Conditions |
|-------|------------|
| **A** | All dimensions pass + description strong + three-layer complete |
| **B** | Required dimensions pass + description weak or body long |
| **C** | Missing STATIC / Execution Flow / Output (one) |
| **D** | Missing name or description |

---

## Metadata (Layer 1)

```yaml
---
name: <unique-id-lowercase-hyphens>
description: "<trigger phrases in EN/CN, colloquial, strong enough to trigger>"
---
```

**Description key points:**
1. Third person: "This skill should be used when..."
2. Specific trigger phrases: "create X", "configure Y"
3. Define boundaries: when to trigger, when not to
4. >250 characters truncated — front-load core use cases
5. Strong enough for model to judge "skill's job, not my job"

**Optional fields:**
```yaml
allowed-tools: [Read, Grep]        # Limit available tools
disable-model-invocation: true      # User-only trigger
agent: "research"                  # Specify subagent type
model: "claude-sonnet-4-6"        # Specify model
```

---

## SKILL.md Body Structure (Layer 2)

```markdown
## STATIC

You are a [<domain expert>], responsibilities are [<core responsibilities>].

### Tool Specifications
#### <tool-name>
- **When to use**: <use case>
- **Required**: <parameters>
- **Note**: <constraints>

### Safety and Constraints
- [Forbidden] <dangerous behavior>
- [Warning] <actions needing confirmation>

---

## Execution Flow

### [Type Detection]
| User Intent | Route |
|---|---|
| "..." | -> Flow A |

### [Flow A]
1. [Prepare] <check and prepare>
2. [Execute] <specific operations>
3. [Verify] <check results>
4. [Report] <structured output>

---

## Output Specification

```json
// Success
{ "action": "...", "result": "success", "details": {} }

// Failure
{ "action": "...", "result": "failed", "error": { "code": "...", "recoverable": false } }
```

---

## references/ Directory (Layer 3)

Extract detailed content from SKILL.md to `references/` when complex:

```
skill-name/
├── SKILL.md
├── references/
│   ├── patterns.md
│   └── api-reference.md
├── scripts/
│   └── validate.sh      # Output goes into context, not source
└── assets/
    └── template.html     # Reference path only
```

---

## Remediation Guide

Apply this when skill-reviewer outputs grade C or D.

### If description fails:
1. Identify the skill's core use case in one sentence
2. List 3-5 trigger phrases in EN and CN (colloquial)
3. State explicitly what this skill does NOT handle
4. Rewrite description to be "stronger" — model should immediately know to trigger

### If body is too long (>500 lines):
1. Move detailed API docs to `references/`
2. Move scripts to `scripts/` — only keep execution results in body
3. Consolidate repetitive sections

### If STATIC section missing:
1. Add `## STATIC` with identity definition
2. Add tool specifications for each tool used
3. Add safety constraints (at least 2 [Forbidden] items)

### If execution flow missing:
1. Identify distinct user intent types → map to branches
2. Each branch: [Prepare] → [Execute] → [Verify] → [Report]
3. Add type detection table at the top

### If output specification missing:
1. Define success JSON with `action`, `result`, `details`
2. Define failure JSON with `action`, `result`, `error: { code, recoverable }`

### If three-layer structure missing:
1. Separate metadata (frontmatter) from body
2. Move detailed docs to `references/`
3. Keep body < 500 lines

---

## Quick Checklist

```
[ ] name + description (Layer 1)
[ ] Description strong (EN/CN triggers, clear boundaries)
[ ] SKILL.md body < 500 lines
[ ] ## STATIC section (identity + tools + safety)
[ ] ## Execution Flow (branches + P/E/V/R)
[ ] ## Output Specification (success + failure JSON)
[ ] references/ for complex content
[ ] !command or {$VAR} for dynamic content (suggested)
[ ] Forbidden items >= 2
```

---

_Version history: v1.0.0 (initial release)_
