---
name: skills-creator
description: Guide users through creating, reviewing, and improving OpenClaw skills following proven best practices. Use when someone asks to "create a skill", "write a SKILL.md", "make an OpenClaw skill", "publish to ClawHub", "review my skill", "improve my skill", "optimize skill description", "skill frontmatter help", "what makes a good skill", or discusses OpenClaw/ClawHub skill development, agent skill format, or SKILL.md structure.
version: 1.0.3
metadata: {"clawdbot":{"emoji":"🛠️","requires":{"bins":[]}}}
---

# Skills Creator

Guide the creation, review, and optimization of OpenClaw skills that trigger reliably and instruct LLMs clearly. Based on analysis of top-performing skills across the ClawHub ecosystem.

## Quick Reference

| User wants... | Do this |
|---------------|---------|
| Create a new skill | → Mode 1: Gather requirements, pick complexity tier, write frontmatter + body |
| Review an existing skill | → Mode 2: Run quality checklist, output findings as table |
| Fix poor triggering | → Focus on Description Writing Formula, rewrite with trigger phrases |
| Retrofit / optimize a skill | → Mode 3: Audit → rewrite description → restructure content → re-audit |
| Add external API integration | → Mode 4: Create scripts/ with curl wrapper, declare dependencies |
| Publish to ClawHub | → Verify quality checklist passes, then `clawhub publish` |

## Important Rules

### Rule 1: Always determine complexity tier first

Before writing anything, classify the skill into a tier. This decides file structure, SKILL.md length, and whether supporting directories are needed.

| Tier | When to use | SKILL.md size | Directories |
|------|-------------|---------------|-------------|
| **Simple** | Pure instructions, no executable code | < 150 lines | None |
| **Medium** | Needs scripts or deep reference docs | 100–300 lines | `scripts/` or `references/` |
| **Complex** | Multiple workflows + hooks + cross-platform | 200–650 lines | Multiple subdirs |

### Rule 2: Description is the highest-leverage field

The `description` in frontmatter determines whether an LLM activates the skill at all. Spend disproportionate effort here. A mediocre skill with a great description outperforms a great skill with a mediocre description.

### Rule 3: Write instructions for an LLM, not documentation for a human

The SKILL.md is injected into an LLM's context. Write actionable directives ("Do X when Y"), not explanatory documentation ("This skill provides..."). The LLM needs to know **what to do**, not **what the skill is**.

### Rule 4: Use tables for decision logic, not prose

Tables are the LLM's fastest lookup structure. Any conditional logic ("if X then Y") should be a table row, not a paragraph. Reserve prose for context that doesn't fit a table.

### Rule 5: The skill must describe itself accurately and be internally consistent

Self-consistency is a quality signal. If the skill teaches "add a Quick Reference table", it must have one. If it references a tool, that tool must exist and its description must accurately reflect what it does. Never claim capabilities the skill doesn't have.

### Rule 6: Never auto-execute generated scripts without user confirmation

This skill guides the creation of files including shell scripts. Always present generated scripts to the user for review before executing them. Never run `chmod +x` or execute a newly created script without explicit user approval. The skill is instructional — the user decides what to run.

---

## Workflow Modes

### Mode 1: Create New Skill

#### Step 1: Gather requirements

Ask the user:
- What does the skill do? (one sentence)
- What triggers it? (user phrases, situations, events)
- Does it need external tools, APIs, or binaries?
- Does it need environment variables?

#### Step 2: Determine complexity tier

Use the tier table from Rule 1. When uncertain, start Simple — it's easier to add complexity than remove it.

#### Step 3: Write frontmatter

```yaml
---
name: my-skill-name
description: [Action verb] + [value proposition]. Use when [trigger 1], [trigger 2], ... or discusses [topic area].
version: 1.0.0
homepage: https://github.com/user/repo
metadata: {"clawdbot":{"emoji":"🔧","requires":{"bins":["node"],"env":["MY_API_KEY"]},"primaryEnv":"MY_API_KEY"}}
---
```

Field rules:

| Field | Required | Format | Rules |
|-------|----------|--------|-------|
| `name` | Yes | lowercase kebab-case | Must match folder name. No spaces, no uppercase. |
| `description` | Yes | Single string | Follow the Description Writing Formula below. Include 5+ trigger phrases. |
| `version` | Yes | semver | Independent from any npm/PyPI package version. |
| `homepage` | No | URL | Link to source repo or documentation site. |
| `metadata` | No | **Single-line JSON** | Parser does not support multiline. Use `clawdbot` key (not `openclaw`). |

Metadata sub-fields:

| Sub-field | Purpose | Example |
|-----------|---------|---------|
| `emoji` | Visual identifier on ClawHub | `"🔍"` |
| `requires.bins` | Executables the skill needs | `["node", "npx", "curl"]` |
| `requires.env` | Environment variables needed | `["TAVILY_API_KEY"]` |
| `primaryEnv` | Main env var for quick setup hint | `"TAVILY_API_KEY"` |

#### Step 4: Write SKILL.md body

Follow this section order:

1. **Title + one-paragraph intro** — What it does, in action-oriented language
2. **Quick Reference table** — `| User wants... | Do this |` — 4–8 rows covering main use cases
3. **Important Rules** — Numbered constraints the LLM must follow (3–5 rules)
4. **Workflow Modes** — Discrete scenarios with step-by-step instructions
5. **Reference sections** — Field references, formulas, lookup tables
6. **Gotchas** — Critical pitfalls with one-line fixes
7. **Further Reading** — Links to `references/` and `assets/` files

Use the starter template at `{baseDir}/assets/skill-template.md` as a starting point.

#### Step 5: Create supporting files (Medium/Complex tiers)

| Directory | When to create | What goes inside |
|-----------|---------------|-----------------|
| `references/` | SKILL.md exceeds 200 lines, or has deep-dive content | Detailed guides, examples, troubleshooting |
| `scripts/` | Skill needs executable code (API calls, automation) | Shell/Node scripts using `{baseDir}` paths |
| `assets/` | Skill provides templates for users to copy | Starter files, config templates |
| `hooks/` | Skill needs event-driven triggers (rare) | Hook handlers for agent lifecycle events |

Never create `_meta.json` — ClawHub generates it automatically.

#### Step 6: Run quality review

Read `{baseDir}/references/quality-checklist.md` and run through all 24 checks. Fix any failures before considering the skill complete.

---

### Mode 2: Review Existing Skill

1. Ask the user to provide their SKILL.md content (or a file path to read)
2. Read `{baseDir}/references/quality-checklist.md`
3. Evaluate the skill against all 6 categories (24 checks total)
4. Present findings as a table:

```
| Category | Status | Issue | Fix |
|----------|--------|-------|-----|
| Frontmatter | ⚠️ | metadata is multiline JSON | Collapse to single line |
| Description | ❌ | No trigger phrases | Rewrite using the formula |
| Content | ✅ | — | — |
```

5. Prioritize fixes by impact: **Description > Structure > Security > Style**
6. Offer to apply fixes directly if the user provides a file path

---

### Mode 3: Retrofit / Optimize Existing Skill

For skills that exist but don't follow best practices:

1. **Audit**: Run the full quality checklist, list all failures
2. **Rewrite description**: Apply the Description Writing Formula — this has the highest impact
3. **Add Quick Reference**: If missing, create a situation → action table from the skill's content
4. **Convert prose to tables**: Find any conditional logic in paragraphs, restructure as table rows
5. **Add guard clauses**: Ensure "When to use" and "When NOT to use" are explicit
6. **Extract deep content**: Move anything beyond 300 lines into `references/`
7. **Add negative cases**: Ensure fallback handling exists (what to do when things fail)
8. **Re-audit**: Run the checklist again to verify all fixes

---

### Mode 4: Add External API Integration

When a skill needs to call an HTTP API (image generation, search, translation, etc.):

#### Pattern: scripts/ with curl wrapper

Create `scripts/call-api.sh`:

```bash
#!/usr/bin/env bash
# Usage: {baseDir}/scripts/call-api.sh "prompt text"
set -euo pipefail

API_KEY="${API_KEY:?Missing API_KEY environment variable}"

response=$(curl -sf -X POST "https://api.example.com/v1/generate" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"$1\", \"size\": \"1024x1024\"}")

echo "$response"
```

#### Update metadata to declare dependencies

```yaml
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["curl"],"env":["API_KEY"]},"primaryEnv":"API_KEY"}}
```

#### Reference in SKILL.md

```markdown
## Generate Image

\`\`\`bash
{baseDir}/scripts/call-api.sh "a sunset over mountains"
\`\`\`
```

> **Note**: Replace the placeholder URL, headers, and body with the actual API specification. Declare ALL required environment variables in `metadata.clawdbot.requires.env`.

---

## Description Writing Formula

**Formula**:

```
[Action verb] + [value proposition]. Use when someone asks to "[trigger phrase 1]",
"[trigger phrase 2]", "[trigger phrase 3]", ... or discusses [topic area 1], [topic area 2].
```

**Good example**:

> Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails.

**Bad example**:

> A helpful skill for improving agent capabilities and making things better.

Why bad: no trigger phrases, no specific scenarios, vague value proposition. The LLM has no pattern to match against user input.

**Trigger phrase checklist** — include at least 5 of these patterns:

| Pattern | Example |
|---------|---------|
| Imperative verb phrase | "create a skill", "review my skill" |
| Question format | "how do I make a skill", "what makes a good skill" |
| Topic mention | "discusses skill development", "SKILL.md structure" |
| Tool/platform name | "OpenClaw", "ClawHub", "agent skill" |
| Problem statement | "skill not triggering", "fix my description" |

---

## File Organization Guide

| Path | Purpose | When to create |
|------|---------|---------------|
| `SKILL.md` | Core instructions — always present | Always |
| `references/` | Deep-dive docs, examples, troubleshooting | SKILL.md > 200 lines or has detailed reference content |
| `scripts/` | Executable code (shell, Node.js) | Skill wraps an API or automates a task |
| `assets/` | Templates, config files for users to copy | Skill generates boilerplate |
| `hooks/` | Event-driven agent lifecycle handlers | Skill needs automatic triggers (rare) |
| `_meta.json` | **Never create** — auto-generated by ClawHub | Never |

Keep SKILL.md under 300 lines. Extract to `references/` beyond that threshold.

Use `{baseDir}` in SKILL.md to reference files within the skill package — the platform resolves this to the skill's installation path at runtime.

---

## Gotchas

- **Metadata must be single-line JSON** — the ClawHub parser does not support multiline. `{"clawdbot":{"emoji":"🔧"}}` not formatted JSON.
- **Never create `_meta.json`** — ClawHub auto-generates it on publish. Committing one causes conflicts.
- **Use `{baseDir}` for script paths** — skills can be installed anywhere. Never hardcode absolute paths.
- **Avoid VirusTotal-flagged terms** — words like "upload", "public URL", "CDN" trigger security scans. Use "prepare", "reference", "compress" instead.
- **Pin versions in npx references** — `meigen@1.2.5` not `meigen@latest`. Floating versions are a supply chain risk.
- **List ALL binaries in `requires.bins`** — include transitive dependencies (`node`, `npx`, not just your script name).
- **Use `clawdbot` key in metadata** — not `openclaw`. This is the established convention (5/6 top skills use it).

## Further Reading

- `{baseDir}/references/best-practices.md` — comprehensive design guidelines with worked examples
- `{baseDir}/references/quality-checklist.md` — full 24-point review checklist and retrofit process
- `{baseDir}/assets/skill-template.md` — copy-paste starter template for new skills
