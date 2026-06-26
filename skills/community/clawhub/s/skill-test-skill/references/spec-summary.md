# Agent Skills Specification Summary

> Source: https://agentskills.io/specification
> Reference: https://github.com/anthropics/skills

This document is a complete reference for validating skills against the official Agent Skills spec. Load it when you need to verify specific rules during a validation run.

---

## Table of Contents

1. [Directory Structure Rules](#1-directory-structure-rules)
2. [SKILL.md Format Rules](#2-skillmd-format-rules)
3. [Frontmatter Field Rules](#3-frontmatter-field-rules)
4. [Body Content Rules](#4-body-content-rules)
5. [Optional Directory Rules](#5-optional-directory-rules)
6. [Progressive Disclosure Rules](#6-progressive-disclosure-rules)
7. [File Reference Rules](#7-file-reference-rules)
8. [Security and Safety Rules](#8-security-and-safety-rules)
9. [Common Errors and Anti-Patterns](#9-common-errors-and-anti-patterns)
10. [Real-World Examples from anthropics/skills](#10-real-world-examples-from-anthropicsskills)

---

## 1. Directory Structure Rules

### Required Structure

```
skill-name/
├── SKILL.md          # REQUIRED: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

### Rules

- **SKILL.md is required.** A skill without SKILL.md is not a valid skill.
- **The directory name must exactly match the `name` frontmatter field.** If the directory is `pdf-processing/`, the name field must be `pdf-processing`.
- **Standard directories and their purposes:**
  - `scripts/` — executable code that agents can run
  - `references/` — documentation that agents read when needed
  - `assets/` — static resources (templates, images, data files)
  - `evals/` — test cases and evaluation data (used by the skill-creator workflow; contains `evals.json` and related files)
  - `agents/` — instructions for specialized subagents (used by complex skills like skill-creator; contains files like `grader.md`, `analyzer.md`, `comparator.md`)
- **Additional files and directories are allowed** as long as they serve a legitimate purpose. Do not flag `evals/` or `agents/` as unexpected — they are standard.

---

## 2. SKILL.md Format Rules

### Required Format

```
---
[YAML frontmatter]
---
[Markdown body]
```

- The file **must** start with a YAML frontmatter block delimited by `---`
- The frontmatter **must** contain at least `name` and `description`
- The Markdown body follows the closing `---`
- There are **no format restrictions** on the body — write whatever helps agents perform the task

### Size Guidance

- Keep SKILL.md under **500 lines** (this is a strong recommendation, not a hard rule)
- If approaching 500 lines, add a layer of hierarchy and point to reference files
- The spec notes: "Consider splitting longer SKILL.md content into referenced files"

---

## 3. Frontmatter Field Rules

### `name` (REQUIRED)

**Constraints:**
- Must be **1–64 characters**
- May only contain: **lowercase letters (a-z)**, **digits (0-9)**, **hyphens (-)**
- Must **not** start with a hyphen
- Must **not** end with a hyphen
- Must **not** contain consecutive hyphens (`--`)
- Must **match the parent directory name** exactly

**Valid examples:**
```yaml
name: pdf-processing
name: data-analysis
name: code-review
name: my-skill-v2
```

**Invalid examples:**
```yaml
name: PDF-Processing      # uppercase not allowed
name: -pdf                # cannot start with hyphen
name: pdf--processing     # consecutive hyphens not allowed
name: pdf_processing      # underscores not allowed
name: pdf processing      # spaces not allowed
name: this-name-is-way-too-long-and-exceeds-the-sixty-four-character-limit-set-by-spec  # too long
```

### `description` (REQUIRED)

**Constraints:**
- Must be **1–1024 characters**
- Must be **non-empty**
- Should describe **what the skill does** AND **when to use it**
- Should include **specific keywords** that help agents identify relevant tasks

**Quality criteria (from spec and skill-creator best practices):**
- Describes the skill's capabilities concretely (not just a label)
- Includes trigger conditions ("Use when...", "TRIGGER when...")
- Contains diverse keywords covering different ways users might phrase the request
- Is slightly "pushy" to prevent undertriggering (Claude tends to undertrigger skills)
- **All "when to use" information belongs here, not in the body.** From skill-creator: "This is the primary triggering mechanism - include both what the skill does AND specific contexts for when to use it. All 'when to use' info goes here, not in the body." The body should focus on *how* to perform the task.

**Good example:**
```yaml
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
```

**Poor examples:**
```yaml
description: Helps with PDFs.                    # Too vague, no trigger conditions
description: A skill.                            # Meaningless
description: Use this for everything.            # Too broad
```

**The "pushy" pattern (from skill-creator):**
Instead of: "How to build a dashboard to display data."
Write: "How to build a dashboard to display data. Make sure to use this skill whenever the user mentions dashboards, data visualization, or wants to display any kind of data, even if they don't explicitly ask for a 'dashboard.'"

### `license` (OPTIONAL)

**Constraints:**
- If present: specifies the license applied to the skill
- Should be short: either a license name or the name of a bundled license file
- Full license text should NOT be inline — reference a bundled file instead

**Examples:**
```yaml
license: Apache-2.0
license: MIT
license: Proprietary. LICENSE.txt has complete terms
license: Complete terms in LICENSE.txt
```

### `compatibility` (OPTIONAL)

**Constraints:**
- If present: must be **1–500 characters**
- Should only be included if the skill has **specific environment requirements**
- Can indicate: intended product, required system packages, network access needs

**Examples:**
```yaml
compatibility: Designed for Claude Code (or similar products)
compatibility: Requires git, docker, jq, and access to the internet
compatibility: Requires Python 3.14+ and uv
```

**When to omit:** Most skills do not need this field. If the skill works in any standard Claude environment, omit it.

### `metadata` (OPTIONAL)

**Constraints:**
- If present: must be a **map from string keys to string values**
- Keys should be reasonably unique to avoid accidental conflicts

**Example:**
```yaml
metadata:
  author: example-org
  version: "1.0"
  category: document-processing
```

### `allowed-tools` (OPTIONAL, EXPERIMENTAL)

**Constraints:**
- If present: a **space-delimited list** of pre-approved tools
- Support for this field may vary between agent implementations

**Example:**
```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read
```

---

## 4. Body Content Rules

### What to Include

The spec says: "Write whatever helps agents perform the task effectively."

**Recommended sections (from spec):**
- Step-by-step instructions
- Examples of inputs and outputs
- Common edge cases

**Best practices (from skill-creator):**
- Use **imperative form**: "Read the file", "Run the script", "Check the output"
- Explain the **why** behind instructions, not just the what
- Define **output formats** clearly with templates or examples
- Use **theory of mind**: write for a smart agent that can generalize, not just follow rigid rules
- Avoid excessive `MUST`, `ALWAYS`, `NEVER` — explain reasoning instead
- **All "when to use" information belongs in the description, not the body.** The body should focus on *how* to perform the task. If you find yourself writing a "When to Use This Skill" section in the body, move it to the description field instead.

### What to Avoid

- Malware, exploit code, or content that could compromise security
- Misleading content that doesn't match the skill's stated purpose
- Overly rigid, narrow instructions that only work for specific examples
- Passive voice when imperative is clearer
- Instructions without rationale (the agent can't generalize from rules alone)

### Size Limits

- **Recommended:** Under 500 lines
- **Acceptable:** 500–600 lines with a note to split content
- **Problematic:** 600–800 lines — should definitely split into references/
- **Critical:** 800+ lines — violates the spirit of progressive disclosure

---

## 5. Optional Directory Rules

### scripts/

Scripts should:
- Be **self-contained** or clearly document their dependencies
- Include **helpful error messages**
- Handle **edge cases gracefully**
- Support `--help` flag where applicable (from webapp-testing example)
- Be designed as **black-box tools** that agents call directly, not read into context

**From webapp-testing SKILL.md:**
> "Always run scripts with `--help` first to see usage. DO NOT read the source until you try running the script first and find that a customized solution is absolutely necessary. These scripts can be very large and thus pollute your context window."

Supported languages depend on the agent implementation. Common: Python, Bash, JavaScript.

### references/

Reference files should:
- Be **focused** on a single topic
- Be **under 300 lines** per file (agents load these on demand; smaller = less context)
- Be **clearly referenced** from SKILL.md with guidance on when to read them
- For large files (>300 lines): include a **table of contents**

**Domain organization pattern (from spec):**
```
cloud-deploy/
├── SKILL.md (workflow + selection logic)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the relevant reference file, not all of them.

### assets/

Assets should:
- Be **static resources**: templates, images, data files, lookup tables, schemas
- Be **actually used** by the skill (don't include unused assets)
- Be appropriate for their type (templates in assets/, not in references/)

---

## 6. Progressive Disclosure Rules

The three-tier loading system:

| Tier | Content | When Loaded | Size Target |
|------|---------|-------------|-------------|
| Metadata | name + description | Always (all skills) | ~100 words |
| Instructions | SKILL.md body | When skill activates | <500 lines recommended |
| Resources | scripts/, references/, assets/ | On demand | Unlimited |

**Key principle:** Keep each tier appropriately sized. The metadata tier is always in context for ALL skills, so it must be concise. The instructions tier is loaded when the skill activates, so it should be complete but not bloated. Resources are loaded only when needed, so they can be large.

**Architectural decision guide:**
- If SKILL.md is approaching 500 lines → move reference material to references/
- If the same code block appears in multiple places → move it to scripts/
- If you have large tables or lookup data → move to assets/ or references/
- If you have domain-specific variants → organize into references/ by domain

---

## 7. File Reference Rules

When referencing other files in a skill, use **relative paths from the skill root**:

```markdown
See [the reference guide](references/REFERENCE.md) for details.
Run the extraction script: `scripts/extract.py`
```

**Rules:**
- Use relative paths, not absolute paths
- Keep file references **one level deep** from SKILL.md
- Avoid deeply nested reference chains (SKILL.md → ref1.md → ref2.md → ref3.md)
- Include guidance on **when** to read each reference file

---

## 8. Security and Safety Rules

From the spec's "Principle of Lack of Surprise":

- Skills **must not** contain malware, exploit code, or content that could compromise system security
- A skill's contents should **not surprise the user** in their intent if described
- Do not create misleading skills or skills designed to facilitate:
  - Unauthorized access
  - Data exfiltration
  - Other malicious activities
- "Roleplay as an XYZ" type skills are acceptable

---

## 9. Common Errors and Anti-Patterns

### Frontmatter Errors

| Error | Example | Fix |
|-------|---------|-----|
| Uppercase in name | `name: MySkill` | `name: my-skill` |
| Underscore in name | `name: my_skill` | `name: my-skill` |
| Hyphen at start/end | `name: -skill` or `name: skill-` | Remove leading/trailing hyphen |
| Consecutive hyphens | `name: my--skill` | `name: my-skill` |
| Name too long | `name: this-is-a-very-long-name-that-exceeds-the-limit` | Shorten to ≤64 chars |
| Name/directory mismatch | dir=`pdf-tool/`, name=`pdf-processor` | Make them match |
| Empty description | `description: ""` | Write a real description |
| Description too vague | `description: Helps with things.` | Be specific about what and when |
| Description too long | 1200 character description | Trim to ≤1024 chars |

### Body Content Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Passive voice instructions | "The skill will process the file" | "Process the file by..." |
| Rules without rationale | "ALWAYS use format X" | "Use format X because it ensures Y" |
| Overfitting to examples | Instructions only work for specific test cases | Generalize with principles |
| Bloated SKILL.md | 800+ line SKILL.md | Move content to references/ |
| Inline large code blocks | 100-line script in SKILL.md | Move to scripts/ |
| No output format | User doesn't know what to expect | Add output template or example |
| Missing edge cases | Only handles happy path | Add edge case guidance |

### Progressive Disclosure Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Everything in SKILL.md | 600+ lines, slow to load | Split into references/ |
| No scripts/ for reusable code | Every invocation reinvents the wheel | Bundle common scripts |
| Deeply nested references | SKILL.md → A.md → B.md → C.md | Keep references one level deep |
| Unused assets | Files in assets/ never referenced | Remove or reference them |

---

## 10. Real-World Examples from anthropics/skills

### Excellent: webapp-testing

```yaml
---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
license: Complete terms in LICENSE.txt
---
```

**Why it's good:**
- Name is lowercase, hyphenated, descriptive
- Description clearly states what it does (Playwright testing) and when to use it (local web apps)
- Has `license` field
- Body uses decision trees and clear patterns
- Has `scripts/` with helper scripts referenced clearly
- Has `examples/` with concrete code examples

### Excellent: mcp-builder

```yaml
---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Complete terms in LICENSE.txt
---
```

**Why it's good:**
- Description covers what (MCP servers), how (FastMCP/TypeScript SDK), and when (building MCP servers, integrating APIs)
- Has `reference/` directory with domain-specific guides (python_mcp_server.md, node_mcp_server.md)
- Body uses phases and clear workflow
- References are loaded on demand, not all at once

### Good: brand-guidelines

```yaml
---
name: brand-guidelines
description: Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
license: Complete terms in LICENSE.txt
---
```

**Why it's good:**
- Specific trigger conditions ("when brand colors or style guidelines apply")
- Concrete capabilities listed (colors, typography)
- Compact SKILL.md with inline reference data (appropriate for this skill's size)

### Template (Minimal Valid Skill)

```yaml
---
name: template-skill
description: Replace with description of the skill and when Claude should use it.
---
# Insert instructions below
```

**Note:** This is the minimal valid structure. A real skill needs a real description and real body content.

### skill-creator Description Optimization Insight

From the skill-creator SKILL.md:
> "Currently Claude has a tendency to 'undertrigger' skills — to not use them when they'd be useful. To combat this, please make the skill descriptions a little bit 'pushy'. So for instance, instead of 'How to build a simple fast dashboard to display internal Anthropic data.', you might write 'How to build a simple fast dashboard to display internal Anthropic data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a dashboard.'"
