---
name: skill-distiller
description: Skill Distiller. Triggered when users encounter repetitive problems, need to systematize a solution in a certain domain, or want to solidify someone's methodology into a reusable operational process.
---

# Skill Distiller

## Trigger Phrases

Methodology solidification, process standardization, experience extraction, pattern refinement, system building.

## Philosophy

> A good skill turns "fuzzy wisdom" into "clear paths."

The essence of any quality skill is a closed loop:
**Problem-Driven → Theory Anchored → Process Solidified → Tools Implemented**

---

## Workflow (Four-Step Method)

### Step 1: Precisely Define the Problem

**Goal**: Clearly articulate "what exactly is the problem" rather than "what you want to do."

**Guiding Questions**:
- How often does this problem occur?
- How much time/energy does this problem consume?
- Have you tried to solve it before? How? Where did you get stuck?
- If this problem were completely solved, what changes would it bring?

**Output Format**:

```
## Problem Definition

### Problem Description
[State it in one sentence]

### Trigger Scenarios
- Scenario A:
- Scenario B:

### Pain Point Severity
[Rated 1-5], impacting [what]

### Known Attempts
| Solution | Effect | Blockers |
|----------|--------|----------|
| ...      | ...    | ...      |
```

---

### Step 2: Find Theoretical Support

**Goal**: Find the "underlying principles" that are documented and logically sound for solving this problem.

**Theory Source Priority**:
1. **Expert Methodologies** — Specific practices of domain experts (e.g., STEP framework from *Contagious*, MECE from *The Pyramid Principle*)
2. **Classic Theories** — Frameworks with academic or practical validation (e.g., AIDA, FOGRA, SMART)
3. **Industry Consensus** — Widely recognized standards in the field
4. **Cross-Domain Transfer** — Logic validated in other domains, transferred to the current problem

**Guiding Questions**:
- In this domain, are there recognized experts or books?
- Are there existing frameworks or formulas that can be used?
- If you were to teach someone else, how would you explain it?

**Output Format**:

```
## Theoretical Support

### Core Theory
- **Theory Name**: [Name it]
- **Source**: [Book/Course/Expert/Original]
- **Core Idea**: State it in one sentence

### Theory Excerpt
> [Key original text]

### How to Apply the Theory
[How this theory solves your problem]

### Additional References
- Reference A:
- Reference B:
```

---

### Step 3: Structure the Process

**Goal**: Turn the theory into an actionable set of steps.

**Principles**:
- Each step is executable and verifiable
- Clear inputs and outputs
- Closed loop: output of previous step is input of next step
- Fallback plans for exceptions

**Guiding Questions**:
- What is the first step?
- After completing the first step, how do you know it was done correctly?
- What is the input for the second step?
- Loop until closed

**Output Format**:

```
## Process Specification

### Process Overview
[Process Name]: [Starting Point] → [Step 1] → [Step 2] → ... → [Closing Point]

### Detailed Steps

#### Step 1: [Step Name]
- **Input**:
- **Action**:
- **Output**:
- **Success Criteria**: [How to know this step is done well]
- **Exception Handling**: [What to do if something goes wrong]

#### Step 2: [Step Name]
... (same structure as above)

### Closed-Loop Validation
- Can you return to Step 1 from the final step? ✅/❌
- Does each step have a clear output? ✅/❌
- Are exceptions handled? ✅/❌
```

---

### Step 4: Provide Execution Tools

**Goal**: Provide tool support for the entire process, enabling automated or semi-automated execution.

**Tool Types**:
- **Information Collection**: Search, RSS, crawlers
- **Content Generation**: Templates, prompts
- **Automation Execution**: Scripts, workflows
- **Storage Management**: Note-taking systems, file structures
- **Validation**: Checklists, evaluation criteria

**Guiding Questions**:
- Which steps in this process are repetitive?
- Which steps can be templated?
- Which steps are currently the most time-consuming?
- To what extent do you want automation?

**Output Format**:

```
## Execution Tools

### Tool Inventory
| Tool | Type | Purpose | Automation Level |
|------|------|---------|------------------|
| ...  | ...  | ...     | ...              |

### Prompt Templates
#### [Scenario Name]
```
[Prompt text]
```

### Templates/Checklists
#### [Template Name]
```
[Template content]
```

### Automation Scripts
- Script Path: [Path]
- Function: [What it does]
- Usage: [How to use it]
```

---

## Skill Output Summary

After completing the four steps, aggregate the output into an executable SKILL.md draft:

```
## [Skill Name]

**One-sentence description**: [What problem does this skill solve]

**Applicable Scenarios**:
- ...

**Process**: Problem → Theory → Process → Tools (detailed in respective sections)

---
[Paste the content from each section here]
```

---

## Usage Tips

1. **Don't have to complete all four steps**: If the user only wants to do one step (e.g., only define the problem), just do that step
2. **Iterate and refine**: Start with a rough version, then refine after using it a few times
3. **Start small**: Distill a small problem first, then gradually expand
4. **Don't overdo tools**: One handy tool is more valuable than ten fancy ones
5. **Be specific about the problem**: "I write slowly" is not a problem; "It takes me 2 hours just to figure out the opening for each short video script" is a problem