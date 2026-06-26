# Pattern 5: Pipeline

## Core Purpose

Force **multi-step sequential execution** with checkpoints, preventing skipping critical steps.

## Use Cases

- Document generation (parse→generate→assemble→QC)
- Code migration/refactoring
- Data transformation workflows
- Multi-stage processing tasks

## Directory Structure

```
skills/doc-pipeline/
├── SKILL.md
├── references/
│   ├── docstring-style.md    # Used in Step 2
│   └── quality-checklist.md  # Used in Step 4
└── assets/
    └── api-doc-template.md   # Used in Step 3
```

## SKILL.md Template

```markdown
---
name: doc-pipeline
description: Generate API documentation from Python source code through multi-step pipeline. Activates when users request to document modules, generate API docs, or create documentation from code.
metadata:
  pattern: pipeline
  steps: 4
  trigger-phrases: [generate docs, document this, create API docs]
---

You are running a documentation generation pipeline. **Strictly execute each step in order, prohibit skipping**.

## ⛔ Global Rules
- **Prohibit** skipping any steps
- **Prohibit** continuing when step fails
- **Prohibit** proceeding to next step without user confirmation (if checkpoint exists)
- After each step completes, show results to user and explain next step

---

## Step 1 — Parse & Inventory Generation

**Task**: Analyze user's Python code, extract all public classes, functions, constants

**Output**:
```
Detected following public API:
- [ ] class UserManager
- [ ] def authenticate_user()
- [ ] def create_session()
- [ ] const MAX_RETRY = 3

Please confirm: Is this the complete public API you want documented?
Anything to add or exclude?
```

**Checkpoint**: ⏸️ Wait for user confirmation

---

## Step 2 — Generate Docstrings

**Task**: Generate docstrings for each function missing documentation

**Prerequisite**: Load `references/docstring-style.md`

**Execution**:
For each function:
1. Generate docstring per style guide
2. Include: parameter descriptions, return values, exceptions, examples

**Output**:
```
Generated docstrings for following functions:

### authenticate_user()
```python
def authenticate_user(username: str, password: str) -> User:
    """Validate user credentials and return user object.
    
    Args:
        username: Username (email format)
        password: User password (plaintext)
    
    Returns:
        User: User object on successful authentication
    
    Raises:
        AuthenticationError: When credentials invalid
    
    Example:
        >>> user = authenticate_user("a@example.com", "pass123")
    """
```

**Checkpoint**: ⏸️ Ask user: "Do these docstrings meet expectations? Need adjustments?"

---

## Step 3 — Assemble Documentation

**Prerequisite**: User confirmed Step 2

**Task**: Load `assets/api-doc-template.md`, compile complete documentation

**Output**: Complete API reference document (Markdown format)

---

## Step 4 — Quality Check

**Task**: Self-check against `references/quality-checklist.md`

**Check Items**:
- [ ] Every public symbol has documentation
- [ ] Every parameter has type and description
- [ ] Every function has at least 1 usage example
- [ ] No spelling errors
- [ ] Consistent formatting

**Output**:
```
Quality Check Results:
✅ All checks passed

OR

⚠️ Found 2 issues:
1. create_session() missing example
2. Spelling error: line 35 "authentcate" → "authenticate"

Auto-fixed, please confirm.
```

**Checkpoint**: ⏸️ Wait for user confirmation

---

## Step 5 — Final Delivery

Present complete document, ask:
"Documentation complete! Need to export to other formats (PDF/HTML) or make other adjustments?"
```

## references/docstring-style.md Template

```markdown
# Docstring Style Guide

## Format Conventions
- Use Google style
- First line: One-sentence summary (start with verb)
- After blank line: Detailed description (optional)
- Args/Returns/Raises/Example sections

## Example
```python
def process_data(data: list[dict], threshold: float = 0.5) -> dict:
    """Process raw data and return aggregated results.
    
    Perform filtering, transformation, and aggregation on input data.
    
    Args:
        data: Raw data list, each element is a dictionary
        threshold: Filtering threshold, range 0-1, default 0.5
    
    Returns:
        Dictionary containing following keys:
        - total_count: Total number of processed data
        - filtered_count: Number after filtering
        - aggregated: Aggregation results
    
    Raises:
        ValueError: When data format invalid or threshold out of range
    
    Example:
        >>> result = process_data([{"value": 1}, {"value": 2}], 0.3)
        >>> result["total_count"]
        2
    """
```

## Prohibited Content
- Don't start with "This function..."
- Don't repeat information already expressed in function name
- Don't use vague words ("might", "perhaps")
```

## references/quality-checklist.md Template

```markdown
# Documentation Quality Checklist

## Completeness
- [ ] All public classes, functions, constants have documentation
- [ ] All parameters have type annotations and descriptions
- [ ] All return values have descriptions
- [ ] All exceptions have descriptions

## Accuracy
- [ ] Example code is executable
- [ ] Parameter descriptions match actual usage
- [ ] No outdated information

## Readability
- [ ] No spelling errors
- [ ] Consistent formatting
- [ ] Consistent terminology

## Usefulness
- [ ] Each function has at least 1 example
- [ ] Complex logic has explanations
- [ ] Has usage scenario descriptions
```

## Variant: Automated Pipeline

Automatic flow without user confirmation:

```markdown
## Automatic Mode

Step 1 → Step 2 → Step 3 → Step 4 → Output

Automatically proceed to next step after each step completes, output results once at the end.
Suitable for high-trust, low-tolerance scenarios.
```

## Variant: Conditional Branching Pipeline

```markdown
## Step 2 — Conditional Processing

If code is Python → Generate Google-style docstrings
If code is JavaScript → Generate JSDoc comments
If code is Verilog → Generate comment headers
```

## Pros & Cons

| Pros | Cons |
|-----|------|
| Controllable flow, stable quality | Many steps, time-consuming |
| Each step independently verifiable | Users need multiple confirmations |
| Easy to locate problem steps | Flow rigid, hard to adjust flexibly |

## Combination with Reviewer

```markdown
## Pipeline + Reviewer

Step 1: Parse
Step 2: Generate
Step 3: Assemble
Step 4: Reviewer review (load checklist to score)
Step 5: If score<8, return to Step 2 to regenerate
Step 6: Deliver
```

---

## Checklist

- [ ] Step sequence is clear
- [ ] Each step has clear input/output
- [ ] Checkpoints clearly marked (⏸️)
- [ ] Has failure handling logic
- [ ] Load references/assets on demand
- [ ] Final output format is clear

---

## Pattern Comparison Summary

| Pattern | Core Characteristics | Best Scenarios |
|-----|---------|---------|
| Tool Wrapper | Load knowledge on-demand | Framework conventions/team agreements |
| Generator | Template filling | Document/report generation |
| Reviewer | Checklist-based review | Code Review/audits |
| Inversion | Interview first, then execute | Tasks with unclear requirements |
| Pipeline | Multi-step + checkpoints | Complex transformation workflows |
