# Skill Writing Best Practices

> A comprehensive guide to writing high-quality AI Agent Skills, grounded in how AI context windows actually work.

---

## 1. The Fundamental Insight: Skills Are Onboarding Guides

> Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as **"onboarding guides" for specific domains or tasks**.

This is the most important insight. Skills are not:
- ❌ Configuration files
- ❌ Code to be executed
- ❌ Documentation to be read
- ❌ Prompt templates

Skills are **onboarding guides** — they teach AI about your specific context, workflow, and conventions. Once AI understands, it acts.

---

## 2. The Three-Layer Loading System

Understanding this system is the foundation of good Skill writing.

### Why Layers Matter

Every token in context has a cost. The loading system lets you optimize for:

1. **What AI must always know** → Level 1 (minimal, always loaded)
2. **What AI needs when relevant** → Level 2 (loaded on trigger)
3. **What AI uses during execution** → Level 3 (never in context)

### The Three Layers

```
┌────────────────────────────────────────────────────┐
│  Level 1: Metadata (name + description)            │
│  • Always in context (every session start)         │
│  • Used by AI to decide "should I trigger?"        │
│  • Target size: <150 tokens (~600 chars)           │
│  • Example: "TDD workflow. Use when writing tests" │
└────────────────────────────────────────────────────┘
                         ↓ AI decides to trigger
┌────────────────────────────────────────────────────┐
│  Level 2: SKILL.md Body                           │
│  • Only loaded when Skill triggers                 │
│  • Contains execution instructions                 │
│  • Target size: <5000 tokens (~20000 chars)      │
│  • Example: "Step 1: write test... Step 2: run"  │
└────────────────────────────────────────────────────┘
                         ↓ AI executes
┌────────────────────────────────────────────────────┐
│  Level 3: scripts/ + references/ + assets/         │
│  • Never loaded into context                       │
│  • Executed directly by tools                     │
│  • No context cost                                │
│  • Example: rotate_pdf.py, api_spec.md, logo.png │
└────────────────────────────────────────────────────┘
```

### What Goes Where

| Content Type | Level | Rationale |
|-------------|-------|-----------|
| Skill name | 1 | Always needed for identification |
| Trigger keywords | 1 | AI decides based on this |
| Tool list | 2 | Needed at execution time |
| Step-by-step instructions | 2 | Execution guidance |
| Error handling | 2 | Execution guidance |
| Output format specs | 2 | Execution guidance |
| Detailed API docs | 3 (references/) | Too long for Level 2 |
| Reusable code | 3 (scripts/) | Executed, not read |
| Templates/assets | 3 (assets/) | Output materials |
| Long examples | 3 (references/) | Context, not instructions |

---

## 3. The Description Is a Trigger

The `description` field is the most critical — and most misused — part of a Skill.

### What It Should Be

A **trigger** — a set of keywords and conditions that help AI decide when to use this Skill.

### What It Should NOT Be

A **manual** — full instructions, explanations, or detailed descriptions.

### Good vs Bad Descriptions

#### ❌ Bad: Too Long (Manual, Not Trigger)

```yaml
description: >
  This is a comprehensive guide to Test-Driven Development using
  the red-green-refactor cycle. First, you need to write a failing
  test that describes the behavior you want. Then write the minimum
  code to make it pass. Then refactor while keeping tests green...
```

**Problems:**
- 200+ tokens in Level 1
- Loaded for ALL sessions, even when TDD isn't needed
- Contains content that belongs in Level 2
- Confuses "when to use" with "how to use"

#### ✅ Good: Clear Trigger (<150 tokens)

```yaml
description: >
  TDD test-driven development workflow. Use when writing new features,
  adding tests, or debugging. Keywords: test-driven, TDD, red-green,
  pytest, unit test.
```

**Why It's Good:**
- <150 tokens
- Clear trigger conditions
- Keywords AI can match
- Execution details are in Level 2

### Description Template

```
[Skill Name] - [What it does] in [when/where to use].
Keywords: [trigger, keywords, separated, by, commas].
```

---

## 4. Concise Is Key

> The context window is a public good. Challenge each piece of information: "Does Claude really need this explanation?"

### The Conciseness Test

For every sentence you write, ask:

1. **Does Claude already know this?** → Delete it
2. **Is this project-specific?** → Keep it
3. **Can it be expressed in fewer words?** → Shorten it
4. **Does it belong in a reference file?** → Move it

### Examples: Before and After

#### ❌ Before: Explaining What AI Knows

```markdown
Claude is a powerful AI assistant that can write code in many languages
including Python, JavaScript, TypeScript, Go, Rust, and more. It has a
broad understanding of software engineering principles...
```

#### ✅ After: Project-Specific Context Only

```markdown
This project uses Python 3.11+. All modules are in src/. Tests go in
tests/ using pytest. Follow PEP 8 style guidelines.
```

---

## 5. Role Setting

At the start of SKILL.md, establish the Skill's role clearly.

### Why Role Setting Matters

Role setting focuses AI's behavior and tone for your specific use case. Even one sentence makes a difference.

### Examples

#### ✅ Good: Clear Role

```markdown
# PDF Processing Skill

You are a document preparation assistant specialized in creating
and editing professional PDF documents.
```

#### ❌ Bad: Generic

```markdown
# PDF Skill

This skill helps with PDF tasks.
```

---

## 6. Examples Over Explanations

### The Example Principle

A well-crafted example communicates more than paragraphs of explanation.

### Example Standards

| Quality | Description |
|---------|-------------|
| **Relevant** | Matches real use cases |
| **Diverse** | Covers edge cases |
| **Structured** | Uses clear input/output format |
| **数量** | 3-5 examples ideal |

### How to Format Examples

Use XML tags to distinguish examples from instructions:

```markdown
## Examples

<example id="create-pdf">
Input: "Create an invoice PDF for Acme Corp, $5000"
Output:
```
Document created: invoice_acme_2024.pdf
Format: A4, professional template
Includes: company header, itemized list, total
```
</example>

<example id="edit-existing">
Input: "Add a watermark to contract.pdf"
Output:
```
Modified: contract_watermarked.pdf
Watermark: "DRAFT" diagonal, 30% opacity
```
</example>
```

---

## 7. Degrees of Freedom

Match instruction specificity to task variability.

### Three Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| **High** | Multiple valid approaches | "Organize files by type or date" |
| **Medium** | Some preferred patterns | "Use pytest fixtures for shared setup" |
| **Low** | Consistency critical | "Always run linter before commit" |

### The Bridge Analogy

Think of AI as exploring a path:
- **Narrow bridge over a cliff** → Low freedom, specific guardrails
- **Open field** → High freedom, multiple routes allowed

---

## 8. Resource Organization

### scripts/ — Executable Code

**Use when:**
- Same code is rewritten repeatedly
- Deterministic execution is critical
- Code needs to be versioned

**Examples:**
- `scripts/rotate_pdf.py` — PDF rotation
- `scripts/format_code.sh` — Code formatting
- `scripts/validate_json.py` — JSON validation

**Benefits:**
- Token efficient
- Deterministic
- Version controlled

### references/ — Documentation

**Use when:**
- Detailed docs AI should reference
- Schema definitions
- API specifications
- Company policies

**Best practices:**
- If >10k words, use grep patterns in SKILL.md
- Each reference file should have a table of contents

### assets/ — Output Resources

**Use when:**
- Templates for output
- Brand assets
- Boilerplate files

**Examples:**
- `assets/invoice_template.docx`
- `assets/logo.png`
- `assets/frontend-template/`

---

## 9. SKILL.md Structure Template

Here's a proven structure for SKILL.md:

```markdown
---
name: skill-name
description: >
  [One-line description] - [what it does]. Use when [trigger condition].
  Keywords: [trigger, keywords].
---

# [Skill Name]

[Role setting paragraph - who is this assistant?]

## When to Use

[Explicit trigger conditions - when should AI invoke this?]

## Instructions

[Step-by-step execution guide]

### [Optional Sub-section]

[Additional details]

## Examples

<example id="1">
Input: [user input]
Output: [expected result]
</example>

## References

- Detailed docs: See [FILE.md](references/FILE.md)
- API reference: See [API.md](references/API.md)
```

---

## 10. Common Mistakes

### Mistake 1: Frontmatter Bloat

```yaml
# ❌ Too many fields
---
name: my-skill
version: 1.0.0
author: John Doe
license: MIT
created: 2024-01-01
tags: [python, data, automation]
---

# ✅ Only required fields
---
name: my-skill
description: >
  Data processing automation. Use when...
---
```

### Mistake 2: Level 1 Contains Level 2 Content

```yaml
# ❌ Description has execution details
description: >
  This skill does X by first doing A, then B, then C,
  following the red-green-refactor pattern...

# ✅ Description is just a trigger
description: >
  X workflow. Use when doing A. Keywords: X, A, workflow.
```

### Mistake 3: No Examples

A Skill without examples produces unpredictable outputs.

### Mistake 4: WAI (Writing About AI)

```yaml
# ❌ WAI
"Claude is a powerful LLM that can understand and generate code..."

# ✅ Direct instructions
"Write all Python functions with type hints and docstrings."
```

### Mistake 5: Nested References

References should be one level deep from SKILL.md, not nested further.

```yaml
# ❌ Too nested
SKILL.md → references/guide.md → references/details.md → ...

# ✅ Flat structure
SKILL.md → references/guide.md
SKILL.md → references/details.md
```

---

## 11. Token Budgeting

A practical framework for managing context cost.

### Recommended Budget per Skill

| Layer | Target Tokens | Maximum |
|-------|--------------|---------|
| Level 1 (description) | <100 | 150 |
| Level 2 (body) | <3000 | 5000 |
| Level 3 (resources) | Unlimited | — |

### Cost Calculation

If you have 10 Skills installed:

```
Level 1 cost: 10 × 100 tokens = 1,000 tokens/session
Level 2 cost: Only triggered Skills × their size
Level 3 cost: 0 (not in context)
```

### Optimization Tips

1. Keep descriptions <100 tokens
2. Move detailed docs to references/
3. Use scripts/ for repeated code
4. Remove WAI content
5. Review Skills quarterly for bloat

---

## 12. Quality Checklist

Before publishing a Skill, verify:

- [ ] Description <150 tokens?
- [ ] Description contains trigger keywords?
- [ ] Description is a trigger, not a manual?
- [ ] SKILL.md has role setting?
- [ ] 3-5 relevant examples included?
- [ ] Examples use structured format?
- [ ] Long docs moved to references/?
- [ ] Repeated code in scripts/?
- [ ] No WAI content?
- [ ] Instructions are step-by-step?
- [ ] Error cases handled?
- [ ] Frontmatter only has name + description?
