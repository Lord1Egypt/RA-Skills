# Quality Standards

Definitions and examples for skill quality requirements.

## Contents

- Metadata Standards
- Content Standards
- Text Standards
- Code Standards
- Severity Levels

---

## Metadata Standards

### Name Standards

| Attribute | Standard | Example |
|-----------|----------|---------|
| **Format** | lowercase, numbers, hyphens | `pdf-processing` ✓ |
| **Style** | gerund (-ing) or action verb | `testing-code` ✓ |
| **Length** | ≤ 64 characters | Avoid: `very-long-skill-name-that-exceeds-limits` |
| **Clarity** | Describes what skill does | Avoid: `utils`, `helper`, `tools` |

**Decision tree:**

    Does name describe the skill's purpose?
    ├─ Yes → Is it < 64 chars?
    │        ├─ Yes → Uses lowercase-hyphen?
    │        │        ├─ Yes → ✓ Good name
    │        │        └─ No → Convert to lowercase-hyphen
    │        └─ No → Shorten
    └─ No → Rename to describe purpose

---

### Description Standards

| Attribute | Standard | Example |
|-----------|----------|---------|
| **Format** | Starts with "Use when..." | `Use when optimizing skills` ✓ |
| **Content** | Triggering conditions only | Avoid workflow summaries |
| **Keywords** | Include key trigger terms | "optimize", "quality", "improve" |
| **Voice** | Third person | "Use when..." not "I help..." |
| **Length** | < 500 characters | Concise and specific |

**What to include in description:**
- ✅ Specific trigger scenarios
- ✅ Problem symptoms skill addresses
- ✅ Key terms for discovery
- ✅ When NOT to use (if applicable)

**What NOT to include:**
- ❌ Workflow steps
- ❌ Implementation details
- ❌ How the skill works
- ❌ First/second person voice

**Quality check:**

Good description:

```yaml
"Use when optimizing existing skills, checking skill quality, or when skills need improvement. Triggers on: skill optimization requests, quality audits, or skill fixes."
```

Bad description:

```yaml
"This skill helps you optimize your skills by running diagnostics, generating reports, and fixing issues." 
# Wrong - doesn't say WHEN to trigger
```

---

## Content Standards

### SKILL.md Length

| Target | Rationale |
|--------|-----------|
| **< 200 lines** | Ideal - frequently loaded skills |
| **< 500 lines** | Maximum - acceptable for complex skills |
| **> 500 lines** | Split into references/ |

**Splitting strategy:**

1. Keep in SKILL.md:
   - Overview and core principle
   - Main workflow steps
   - Quick reference
   - Navigation to detailed content

2. Move to references/:
   - Detailed checklists
   - Comprehensive examples
   - API documentation
   - Domain-specific patterns

---

### Progressive Disclosure Pattern

**Level 1: Metadata** (always loaded)

```yaml
name: improving-skills
description: Use when optimizing existing skills or checking quality
```

**Level 2: SKILL.md body** (loaded when triggered)

```markdown
# Improving Skills

## Overview
[Core principle - 1-2 sentences]

## Workflow
[Sequential steps]

## Quick Reference
[Key actions table]
```

**Level 3: References** (loaded as needed)

    **Detailed checklist**: See [diagnostic-checklist.md](diagnostic-checklist.md)
    **Quality standards**: See [quality-standards.md](quality-standards.md)

---

### File Organization Standards

**Good structure:**

    skill-name/
    ├── SKILL.md              # Core workflow
    └── references/
        ├── topic-a.md        # Detailed content A
        └── topic-b.md        # Detailed content B

**Bad structure:**

    skill-name/
    ├── SKILL.md
    ├── README.md             # ❌ Unnecessary
    ├── CHANGELOG.md          # ❌ Unnecessary
    └── docs/
        └── setup.md          # ❌ Too deep

---

### Reference Depth

**Maximum depth:** 1 level from SKILL.md

    SKILL.md → references/file.md  ✓
    SKILL.md → refs/a.md → refs/b.md  ✗ (2 levels)

**Why:** Deep nesting causes partial reads and incomplete information.

---

## Text Standards

### Conciseness Principles

| Principle | Check |
|-----------|-------|
| **Earn tokens** | Does each sentence justify its presence? |
| **No basics** | Can Claude know this already? |
| **No redundancy** | Is this said elsewhere? |
| **Active voice** | Is it direct and clear? |

**Before optimization (100 tokens):**

PDF (Portable Document Format) files are a common format that contains
text and images. To extract text from a PDF, you'll need to use a 
library. There are many libraries available, but we recommend pdfplumber
because it's easy to use and handles most cases well.

**After optimization (30 tokens):**

Use pdfplumber for PDF text extraction.

**Token savings:** 70%

---

### Assumption Guidelines

**Assume Claude knows:**
- Basic programming concepts
- Common file formats
- Standard libraries
- General best practices

**Do NOT assume Claude knows:**
- Project-specific conventions
- Company internal tools
- Custom schemas
- Domain-specific patterns

**Example:**

✓ Good - assumes basics:

Use pdfplumber:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

✗ Bad - over-explains basics:

PDF files are documents. Python has libraries. pdfplumber is one such 
library. You can install it with pip install pdfplumber. Then import it...

---

### Terminology Standards

| Good Practice | Bad Practice |
|---------------|--------------|
| Use one term consistently | Mix synonyms |
| Define terms once | Repeat definitions |
| Use domain-standard terms | Invent new terms |

**Example:**

✓ Consistent terminology:

"Use the `endpoint` to fetch data. Configure the `endpoint` URL in settings."

✗ Inconsistent terminology:

"Use the `endpoint` to fetch data. Configure the `URL` in settings. 
Access the `route` for updates."

---

### Timelessness Standards

**Avoid:**
- Specific dates ("before August 2025")
- Version numbers without context ("use version 2.3")
- Temporary states ("currently supported")

**Instead use:**
- Feature-based distinctions ("Use v2 API for async support")
- Deprecation patterns ("Old patterns" section)
- Capability descriptions ("Supports OAuth 2.0")

**Pattern:**

## Current Method
[Recommended approach]

## Old Patterns
<details>
<summary>Legacy approach (deprecated DATE)</summary>
[Historical context only]
</details>

---

## Code Standards

### Error Handling Standards

**Required for:**
- File operations
- Network requests
- User input
- External dependencies

**Pattern:**

```python
try:
    # Operation
    result = perform_action()
except SpecificError as e:
    # Handle specific error
    print(f"Helpful message: {e}")
    result = fallback_value()
```

**Error message quality:**

| Good | Bad |
|------|-----|
| "File not found: {path}. Creating default." | "Error" |
| "API rate limit reached. Waiting 60 seconds." | "Failed" |
| "Invalid config: missing 'api_key'. See [config.md](config.md)" | "Config error" |

---

### Constant Documentation

**Magic number:**

```python
TIMEOUT = 47  # Why 47?
```

**Documented constant:**

```python
# Average API response time is 5 seconds
# Timeout is 3x average to handle slow connections
REQUEST_TIMEOUT = 15
```

**Justification requirements:**
- Why this value?
- What factors influenced it?
- When should it change?

---

### Dependency Standards

**Declaration format:**

**Required:**
- `pdfplumber >= 0.10.0` - PDF text extraction
- `pillow >= 10.0` - Image processing

**Install:**

```bash
pip install pdfplumber pillow
```

**Verify installation:**

```bash
python -c "import pdfplumber; print(pdfplumber.__version__)"
```

**What to include:**
- Package name and version requirement
- Purpose of each dependency
- Installation command
- Verification method

---

## Severity Levels

### HIGH Severity

**Definition:** Prevents skill discovery or execution

**Examples:**
- Name format violations
- Description missing "Use when"
- Missing error handling in critical scripts
- Windows-style paths

**Action:** Must fix immediately

---

### MEDIUM Severity

**Definition:** Impacts quality or usability

**Examples:**
- SKILL.md over 500 lines
- Missing keywords in description
- Verbose explanations
- Undocumented constants

**Action:** Should fix soon

---

### LOW Severity

**Definition:** Minor improvement

**Examples:**
- Terminology inconsistency
- Missing table of contents
- Non-optimal examples

**Action:** Nice to fix

---

## Quality Scoring

### Grade Calculation

**A (Excellent):**
- All HIGH items pass
- < 2 MEDIUM items fail
- No critical issues

**B (Good):**
- All HIGH items pass
- < 5 MEDIUM items fail
- No critical issues

**C (Acceptable):**
- All HIGH items pass
- Any number of MEDIUM items fail
- Minor issues only

**D (Needs Work):**
- Any HIGH item fails
- Multiple critical issues

**F (Broken):**
- Multiple HIGH items fail
- Critical issues prevent use

---

### Score Improvement Path

1. Fix all HIGH severity items
2. Address critical MEDIUM items
3. Verify fixes with tests
4. Re-score
5. Document improvements
