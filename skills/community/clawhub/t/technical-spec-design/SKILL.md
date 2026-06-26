---
name: technical-spec-design
description: >
  Transforms product requirements into structured technical specifications.
  Auto-triggers when requirements are unclear, multiple implementation approaches
  exist, or component-level/architecture design is needed.

  Auto-trigger conditions:
  - User asks "how to implement a feature"
  - Requests design of technical specs / architecture / APIs / components
  - Mentions "multiple implementation approaches, need comparison"
  - Provides PRD / requirements description, wants technical specs
  - Requirements contain uncertainty or ambiguity

  NOT applicable for:
  - Simple bug fixes
  - Simple features with clear implementation path
  - Pure coding tasks (no design decisions)
---

# Installation


## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

**Via ClawdHub (recommended):**
```bash
clawdhub install technical-spec-design
```

**Manual:**
```bash
git clone https://github.com/wjszxli/technical-spec-design ~/.openclaw/skills/technical-spec-design
```

# Technical Specification Design Skill

## 1. Input Contract

Accepts the following input types:

1. Complete PRD document
2. Brief requirements description (may be incomplete)
3. Existing technical specification (for optimization/review)

---

## 2. Available Resources

### Core Templates

| Resource                                                                               | Purpose              | Usage Scenario                |
| ---------------------------------------------------------------------------------- | -------------------- | ----------------------------- |
| [`spec_template.md`](resources/spec_template.md)                                   | Main spec template   | Starting new technical specs  |
| [`component_template.md`](resources/component_template.md)                         | Component design     | Designing individual components|
| [`requirements_analysis_template.md`](resources/requirements_analysis_template.md) | Requirements analysis | Breaking down requirements    |

### Examples

| Resource                                                     | Purpose          |
| -------------------------------------------------------- | ------------- |
| [`examples/sample_input.md`](examples/sample_input.md)   | Sample PRD input |
| [`examples/sample_output.md`](examples/sample_output.md) | Complete spec example  |

### Scripts

| Script                                                   | Purpose           | Usage                                                               |
| ------------------------------------------------------ | -------------- | ------------------------------------------------------------------ |
| [`scripts/generate_spec.py`](scripts/generate_spec.py) | Generate spec from template | `python scripts/generate_spec.py --interactive -o my_spec.md` |
| [`scripts/validate.py`](scripts/validate.py)           | Validate skill structure   | `python scripts/validate.py`                                |

---

## 3. Output Contract

Output must be Markdown and strictly include the following structure (may be trimmed by mode):

### Standard Structure

1. Requirements Clarification (if needed)
2. Requirements Analysis (the trifecta)
3. Technical Specification Design
4. Component/Module Design
5. Technology Selection Comparison (if applicable)
6. Risk and Boundary Analysis
7. Pending Questions

---

## 4. Mode System (Auto-selected)

### Mode A: Requirements Clarification Mode
Trigger conditions:
- Insufficient input information
- Key uncertainties exist

Output:
- Only output "Requirements Clarification Questions"
- Do not proceed with any design work

---


### Mode B: Lightweight Specification Mode
Trigger conditions:
- Simple features
- Implementation path is relatively clear

Output:
- Simplified requirements analysis
- Core specification design
- Brief component breakdown

---

### Mode C: Full Technical Specification Mode (Default)
Trigger conditions:
- Medium to large requirements
- Involves architecture/component design/technology selection

Output complete structure

---

## 5. Execution Flow (Must Follow Strictly)

### Step 1: Requirements Completeness Check

Check for missing information:
- User goals
- Requirements context
- Inputs and outputs
- Constraints
- Edge cases

If missing:
→ Enter Mode A, output only clarification questions

---

### Step 2: Requirements Analysis (The Trifecta)

#### 1. Feature Breakdown
Format:
Product requirement → Page/Module → Change points

#### 2. Use Case Analysis
Describe complete user paths (cross-page)

#### 3. Page Operation Specification
Format:
Action + Condition + Object + Behavior

---

### Step 3: Technical Specification Design

Include:

- Architecture breakdown (frontend/backend/services)
- Data flow design
- State management
- Core processes (pseudocode acceptable)

---

### Step 4: Component/Module Design

Requirements:

- Must drill down to component/module level
- Clear responsibility boundaries
- Describe dependencies

---

### Step 5: Technology Selection Comparison (If Multiple Options)

Must use table format:

| Approach | Description | Pros | Cons | Use Cases |

---

### Step 6: Risk and Boundary Analysis

Must include:

- Edge cases
- Performance concerns
- Scalability
- Exception handling

---

### Step 7: Output Pending Questions

List all issues still requiring product/business confirmation

---


## 6. Output Constraints (Mandatory)

### Prohibited

- ❌ Output runnable code (JS / TS / Java / SQL, etc.)
- ❌ Skip requirements analysis and write specs directly
- ❌ Make assumptions based on "common cases"
- ❌ Use vague language (e.g., "maybe", "typically")

---

### Required

- ✅ Use structured expression
- ✅ Use pseudocode for process descriptions
- ✅ All changes must map to components/modules
- ✅ Explicit boundaries and exceptions

---

## 7. Technology Research Guidelines

When multiple approaches exist, must use comparison tables—plain text descriptions are not allowed.

---

## 8. Red Flags (Must Stop)

If any of these thoughts occur, must stop and return to the process:

- "Just write a rough spec first"
- "Handle it the common way"
- "Design while coding"
- "This requirement is simple, no analysis needed"

---

## 9. Quick Checklist

Before output, must confirm:

- [ ] Requirements clarified
- [ ] Trifecta complete
- [ ] Component design included
- [ ] Pseudocode used
- [ ] Edge cases analyzed
- [ ] Pending questions documented

---

## 10. Examples (Few-shot)

### Example 1: Ambiguous Requirements (Mode A)

Input:
"Build a comment feature"

Output:
- Do comments support replies?
- Is pagination needed?
- Is liking/upvoting needed?
- Is moderation required?

---

### Example 2: Simple Requirements (Mode B)

Input:
"Show success message after form submission"

Output:
- Brief feature breakdown
- State transitions
- Toast/notification component design

---

### Example 3: Complex Requirements (Mode C)

Input:
"Design an admin system with multi-role permissions"

Output:
Complete technical specification structure (including technology comparison)

---

## Core Principles (Summary)

> The essence of technical specifications: eliminate uncertainty before coding.
