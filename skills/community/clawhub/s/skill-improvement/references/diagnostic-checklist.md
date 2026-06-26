# Diagnostic Checklist

Complete checklist for analyzing skill quality issues.

## Contents

- Metadata Checks (6 items)
- Content Architecture Checks (5 items)
- Text Quality Checks (5 items)
- Code & Tools Checks (5 items)

---

## Metadata Checks

### M1: Name Format

**Check:** Name uses lowercase letters, numbers, and hyphens only

**Valid examples:**
- `pdf-processing` ✓
- `data-validation-2` ✓
- `api-testing` ✓

**Invalid examples:**
- `PDF_Processing` ✗ (contains uppercase and underscore)
- `skill (v2)` ✗ (contains parentheses and space)
- `my-skill!` ✗ (contains special character)

**Severity:** HIGH

**Why it matters:** Claude's skill discovery system expects consistent naming. Non-standard names may not be recognized.

---

### M2: Name Style

**Check:** Name uses gerund form (-ing) or action-oriented

**Good examples:**
- `improving-skills` ✓ (gerund)
- `testing-code` ✓ (gerund)
- `validate-data` ✓ (action verb)

**Avoid:**
- `pdf` ✗ (too vague)
- `utils` ✗ (generic)
- `helper` ✗ (unclear purpose)

**Severity:** MEDIUM

**Why it matters:** Active names clearly communicate what the skill does.

---

### M3: Description Format

**Check:** Description starts with "Use when..."

**Good:**

```yaml
description: Use when optimizing existing skills or checking skill quality
```

**Avoid:**

```yaml
description: This skill helps you improve skills  # Wrong - doesn't say WHEN
description: Optimizes skills  # Wrong - summarizes action, not trigger
```

**Severity:** HIGH

**Why it matters:** Description is the primary trigger mechanism. "Use when" format clearly signals when to load this skill.

---

### M4: Description Content

**Check:** Description describes triggering conditions, NOT workflow

**Good:**

```yaml
description: Use when optimizing existing skills, checking skill quality, or when skills have obvious issues
```

**Bad:**

```yaml
description: Use when optimizing skills - analyzes metadata, checks architecture, generates reports, and validates fixes  # Wrong - summarizes workflow
```

**Severity:** HIGH

**Why it matters:** Claude reads description to decide if skill is relevant. Workflow summaries cause Claude to follow description instead of reading full skill.

---

### M5: Keyword Coverage

**Check:** Description includes key trigger terms

**Required keywords for this skill:**
- "optimize" / "optimizing"
- "skill quality"
- "improve" / "improving"

**Good:**

```yaml
description: Use when optimizing existing skills, checking skill quality, or when skills need improvement
```

**Bad:**

```yaml
description: Use when working with skills  # Too vague, missing specific triggers
```

**Severity:** MEDIUM

**Why it matters:** Keywords enable discovery. Without them, Claude won't find the skill when needed.

---

### M6: Third Person Voice

**Check:** Description written in third person

**Good:**

```yaml
description: Use when optimizing existing skills
```

**Bad:**

```yaml
description: I help you optimize skills  # First person
description: You can use this to optimize skills  # Second person
```

**Severity:** HIGH

**Why it matters:** Description is injected into system prompt. Inconsistent voice causes discovery problems.

---

## Content Architecture Checks

### A1: File Length

**Check:** SKILL.md under 500 lines

**How to verify:**

```bash
wc -l SKILL.md
```

**If over 500 lines:**
- Split content into `references/` files
- Keep core workflow in SKILL.md
- Link to references with "See [filename.md](filename.md)"

**Severity:** MEDIUM

**Why it matters:** Long files consume context window unnecessarily.

---

### A2: Progressive Disclosure

**Check:** Uses progressive disclosure pattern

**Pattern 1 - High-level guide:**

    ## Quick Start
    [Brief code example]
    
    ## Advanced Features
    - **Forms**: See [FORMS.md](FORMS.md)
    - **API**: See [REFERENCE.md](REFERENCE.md)

**Anti-pattern:**

    ## All Features
    [50 lines of detailed API documentation that should be in separate file]

**Severity:** MEDIUM

**Why it matters:** Claude loads files on-demand. Progressive disclosure saves context until needed.

---

### A3: Reference Depth

**Check:** File references at most one level deep

**Good:**

    # SKILL.md
    See [advanced.md](advanced.md)

**Bad:**

    # SKILL.md
    See [advanced.md](advanced.md)
    
    # advanced.md
    See [details.md](details.md)  # Second level - too deep

**Severity:** MEDIUM

**Why it matters:** Deeply nested references may be partially read, causing incomplete information.

---

### A4: Table of Contents

**Check:** Files > 100 lines have table of contents

**Format:**

    # Title
    
    ## Contents
    - Section 1
    - Section 2
    - Section 3
    
    ## Section 1
    ...

**Severity:** LOW

**Why it matters:** TOC enables scanning and navigation for long files.

---

### A5: Workflow Clarity

**Check:** Workflow steps are clear and sequential

**Good:**

    ## Workflow
    
    1. Diagnose skill
    2. Generate report
    3. User selects issues
    4. Execute fixes
    5. Verify results

**Bad:**

    ## Workflow
    There are several things you can do with this skill. First you might want to...

**Severity:** HIGH

**Why it matters:** Clear steps prevent confusion and ensure process is followed correctly.

---

## Text Quality Checks

### T1: Token Justification

**Check:** Each paragraph earns its tokens

**Question to ask:** "Does Claude really need this explanation?"

**Remove:**
- Basic concept explanations (Claude knows what PDFs are)
- Obvious step descriptions ("Then save the file")
- Redundant restatements

**Severity:** MEDIUM

**Why it matters:** Context window is a public good. Every token costs.

---

### T2: Assumption Check

**Check:** Assumes Claude knows basics

**Good:**

Use pdfplumber for text extraction:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

**Bad:**

PDF files contain text and images. To extract text, you need a library. pdfplumber is a good library. First install it with pip. Then you can...

**Severity:** MEDIUM

**Why it matters:** Claude already knows what PDFs are and how Python libraries work.

---

### T3: Terminology Consistency

**Check:** Same term used throughout

**Good:**
- Always "API endpoint"
- Always "field"
- Always "extract"

**Bad:**
- Mix "API endpoint", "URL", "route", "path"
- Mix "field", "box", "element"
- Mix "extract", "pull", "get"

**Severity:** LOW

**Why it matters:** Consistency reduces cognitive load.

---

### T4: Timeless Content

**Check:** No time-sensitive information

**Bad:**

If you're doing this before August 2025, use the old API.
After August 2025, use the new API.

**Good:**

## Current Method
Use v2 API endpoint

## Old Patterns
<details>
<summary>Legacy v1 API (deprecated)</summary>
[Historical context]
</details>

**Severity:** MEDIUM

**Why it matters:** Time-sensitive information becomes wrong and misleading.

---

### T5: Concrete Examples

**Check:** Examples are specific, not abstract

**Good:**

**Example:**
Input: "Rotate this PDF 90 degrees"
Output: `python scripts/rotate.py input.pdf --degrees 90`

**Bad:**

**Example:**
Do something appropriate based on the user's request

**Severity:** MEDIUM

**Why it matters:** Concrete examples demonstrate exactly what to do.

---

## Code & Tools Checks

### C1: Error Handling

**Check:** Scripts include explicit error handling

**Good:**

```python
try:
    with open(path) as f:
        return f.read()
except FileNotFoundError:
    print(f"File {path} not found, creating default")
    with open(path, "w") as f:
        f.write("")
    return ""
```

**Bad:**

```python
return open(path).read()  # No error handling
```

**Severity:** HIGH

**Why it matters:** Scripts should solve problems, not create them.

---

### C2: Justified Constants

**Check:** No "magic numbers"

**Good:**

```python
# HTTP requests typically complete within 30 seconds
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed
MAX_RETRIES = 3
```

**Bad:**

```python
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```

**Severity:** MEDIUM

**Why it matters:** Unexplained values are confusing and hard to maintain.

---

### C3: Dependency Declaration

**Check:** Dependencies explicitly declared

**Good (in SKILL.md):**

**Required packages:**
- `pdfplumber` - PDF text extraction
- Install: `pip install pdfplumber`

**Bad:**

```python
import pdfplumber  # Not mentioned anywhere
```

**Severity:** HIGH

**Why it matters:** Claude needs to know what to install.

---

### C4: Unix Paths

**Check:** Uses forward slashes in paths

**Good:**
- `scripts/helper.py`
- `references/guide.md`

**Bad:**
- `scripts\helper.py` (Windows-style)
- `references\guide.md`

**Severity:** HIGH

**Why it matters:** Unix paths work everywhere. Windows paths fail on Unix.

---

### C5: Validation Steps

**Check:** Critical operations have verification

**Good:**

## Workflow
1. Make edits
2. **Validate immediately**: `python validate.py`
3. If validation fails, fix and retry
4. Only proceed when validation passes

**Bad:**

## Workflow
1. Make edits
2. Done

**Severity:** HIGH

**Why it matters:** Validation catches errors before they propagate.

---

## Using This Checklist

1. Run through each check category
2. Mark items as ✓ (pass) or ✗ (fail)
3. For each ✗, record:
   - Location in skill
   - Current state
   - Expected state
   - Severity level
4. Prioritize HIGH issues first
5. Present findings in diagnostic report format
