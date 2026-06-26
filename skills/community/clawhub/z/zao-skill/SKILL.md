---
name: zao-skill
description: >
  Create, design, review, and self-improve agent skills following best practices.
  Use when the user asks to create, write, edit, improve, review, or package a skill;
  also use when describing a new capability that should be turned into a skill;
  or when asking about skill design and structure.
---

# Zao Skill

## Overview (Purpose/Quick Start)

This skill guides the creation, review, and self-improvement of effective skills.

The Overarching Process: 
   → Read Overview and Critical Directives 
   → Follow Workflows with Pre-Step Rationalization Bias Check 
   → After run and before exit:
      1. Meta Evolution Check 
      2. Exit Verification

---

## Core Principles

### 1. Concise is Key

**Default assumption: the agent is already smart.** Only add context it doesn't have. The context window is a public good. Every token in your skill competes for the agent’s attention with conversation history, system context, and other active skills. Focus on what the agent wouldn’t know without your skill.

**Prefer concise examples over verbose explanations.** Challenge each piece in your skill: "Does the agent really need this explanation?" or “Would the agent get this wrong without this instruction?” If the answer is no, cut it. 

### 2. Progressive Disclosure

**Anatomy of a Skill**
```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions body
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

Skills use a three-level loading system and should be structured to take advantage of this progressive disclosure mechanism:

 1. Metadata (name + description) - Always in context (~100 words)
 2. SKILL.md body - In context whenever skill triggers (<500 lines ideal)
 3. Bundled resources - As needed (unlimited, scripts can execute without loading)

**Progressive Rules**

- Keep SKILL.md body under 500 lines; if approaching this limit, split into Bundled Resources and link them from SKILL.md with clear "when to read" guidance
- Keep file references one level deep from SKILL.md and for large reference files (>300 lines), include a table of contents
- Avoid duplication: Each reference MUST add genuinely new value — never repeat what SKILL.md already says.
- The agent reads only the relevant reference file. So keep reference files focused.

**Example: Domain organization**

When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

### 3. Files Are Truth — Read, Don't Recall

The file on disk is the canonical source for rules and procedures; Context and memory are stale shadows — they are frozen at load time. 

---

## Workflows and Output Formats

Apply the bias check before every operation, then jump to your entry point.

### Pre-Step Rationalization Bias Check (before every step operation)

1. **Re-read.** Files may be revised without your notice — every operation guided by a file requires a fresh read of that file.
2. **Follow references.** If the step says "see references/...", no spot-check, no cognitive laziness. Read every detail.
3. **Check completion.** Review the completed work and re-engage the missing steps —  don't assume done after one sub-task, no closure seeking.

Jump to the phase that matches your need to start.

### Process Overview

```
Start → User Need?
   ├─ Create new skill              → Phase 1: Design
   ├─ Draft / update / edit skill   → Phase 2: Drafting
   ├─ Review / validate             → Phase 3: Validation
   └─ Package for release           → Phase 4: Packaging
```

Jump to the phase that matches your current need.

### Phase 1: Design

#### Step 1. Understand intent and extract workflow

**1.1 Workflow ready?**

   - **If the conversation does not contain a relevant workflow** → Follow `references/design-gate.md` Part 1 Init Design Step 1 to 4, to walk through a real workflow.

   - **If already contains** (e.g., "turn this into a skill") → Follow `references/design-gate.md` Part 1 Init Design Step 1 to 3, to interview the user for anything unclear.

   - **Output**: Write to `<skill-name>/.wip/workflow-extraction.md`, covering user goal, triggers, successful steps, failures/corrections, input/output formats, tools, and any project‑specific facts/doc/conventions, or constraints.   

**1.2 Explicit Confirmation for next step**
   LOOP:
      ask "Search for existing similar skills(local repos / online platforms) to enhance our initial design? (yes/no)"      
      if response is yes → go to Step 2
      else if response is no → go to Phase 2
      else:
         handle the user's request normally
         continue LOOP      
 
#### Step 2. Search for similar skills and enhance the design

**2.1 Search**: Follow `references/search-compare.md` to execute search.
  - If nothing is found → inform the user and proceed to Phase 2.

**2.2 Present the summary and Ask**, "Adjust and enhance the design using these results?" 
   - **If the user doesn't want to enhance** → Proceed to Phase 2.
   - **Enhance** → Follow `references/design-gate.md` Part 2 Enhance Design.
     Then proceed to Phase 2.

- **Output Updated**: `<skill-name>/.wip/workflow-extraction.md` updated with Design Context.

---

### Phase 2: Draft the Skill.md

**Entry**: Read `<skill-name>/.wip/workflow-extraction.md`. 

**For a new skill** — create the directory structure as shown in the Anatomy diagram above.

**For an existing skill** — work directly on the existing files.

**Either way** — ensure git tracking from the start.

#### **2.1 Draft Frontmatter (Required)**

```md
---
name: skill-name-in-kebab-case
description: Brief description of capability. Use when [specific triggers].
---
```
   **Frontmatter Rules**:
   - name: skill identifier.
   - description: Start with what the skill does, then include one or more clear "Use when" trigger conditions. Maximum 1024 characters. All "when to use" info goes here, not in the markdown instructions.

   **Purpose**:
   - Under progressive disclosure, the description is **the only thing the agent sees** when deciding which skill to load. 
   - It carries the entire burden of skill triggering.

   **Writing Patterns**
   - Use imperative phrasing
   - Explicitly list contexts where the skill applies
   - Focus on user intent, not implementation steps

   **Example**:
   - Bad example: "How to build a simple fast dashboard to display internal Anthropic data."
   - Good example: "How to build a simple fast dashboard to display internal Anthropic data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"


#### **2.2 Draft Body Sections and Bundled Resources**

**Writing Rules**

- Follow Core Principles. Be concise and use progressive disclosure. Every section must justify its inclusion — if removing it wouldn't change agent behavior, remove it
- Try to explain to the model why things are important in lieu of heavy-handed MUSTs in workflow section. 
- Use theory of mind and try to make the skill general and not super-narrow to specific examples.


**Standard Sections for Skill Creation**

The frontmatter contract above is required. The section layout below is a recommended pattern, not a rigid template: equivalent headings are acceptable when they serve the same purpose clearly.

Suggested template **for the target skill**:
```md
# Skill Name

## Overview 
[Purpose + Scope/Exclusion (+ Minimal working example)]

[Must have:] The Overarching Process: 
   → Read Overview and Critical Directives 
   → Follow Workflows with Pre-Step Rationalization Bias Check 
   → After run and before exit:
      1. Meta Evolution Check 
      2. Exit Verification

## Critical Directives
- [Core Principles/Critical Rules/Entry Behaviour and Constraints, serving as mandatory quality gates at entrance]
- [Last point:] Files Are Truth — Read, Don't Recall
   The file on disk is the canonical source for rules and procedures; Context and memory are stale shadows — they are frozen at load time. 
 

## Workflows and Output Formats (see Workflows Detail Guide below)

### Pre-Step Rationalization Bias Check (before every step operation) [Must have:]

1. **Re-read.** Files may be revised without your notice — every operation guided by a file requires a fresh read of that file.
2. **Follow references.** If the step says "see references/...", no spot-check, no cognitive laziness. Read every detail.
3. **Check completion.** Review the completed work and re-engage the missing steps —  don't assume done after one sub-task, no closure seeking.

[The heart of the skill, step-by-step processes]
[Output Template / Bullets / Example]


## After Completing the Requested Workflow: Evolution Check (Effective Post-Usage)

**Trigger**: Agent self-checks after each run: 
 did it produce a repeatable fix or a meaningful improvement?  
- If uneventful, skip. 
- If yes → follow `references/skill-evolution.md` to maintain following tables.

### Critical Gotchas
| ID | Issue / Symptom | Fix |
|----|----------------|-----|
| ...|...|...|

### Success Patterns
| Date | Change | Context | Result |
|------|--------|---------|--------|
| -- | -- | -- | -- |


## Exit Verification 
[Before Exit, do the overall verification: follow `references/verification-gate.md` to devise the checks.]
| Check | Evidence |
|-------|----------|
| [ ] Exit criteria | [e.g., reviewed trigger list] |


## Advanced features

[Link to separate resources files: See [...]]

```
**Workflows Detail Guide**
   - Start with a process overview – Use TL;DR, decision tree, or concise ASCII flowchart at decision points
   - Break operations into numbered, actionable phases or steps, include working examples where they help
   - Match specificity to the task's fragility. Most skills have a mix to calibrate:
      - Give the agent freedom when multiple approaches / variation are permitted — explain the goal and logic to explore
      - Use pseudocode for complex conditional and algorithmic logic, etc. to improve precision and sequence consistency over plain text
      - Add utility scripts for deterministic, code-repetitive and error-prone tasks (e.g., validation, formatting), scripts handle errors explicitly and reduce variability.
   - Split long SKILL.md content into referenced files under Progressive Disclosure Structure Rules.
  
**Input and Output**: 
   - Use checklists for complex tasks to avoid skipping steps, especially when steps have dependencies or validation gates.
   - Use predefined templates for rigid output; Use bullet points to guide flexible output; Add quick examples if needed.
   - Can be used as quality gates between phases/steps
   - Consider user confirmation checkpoints when necessary.
   
   ```md
   ## Quick Example 1: Report structure
   ALWAYS use this exact template:
   # [Title]
   ## Executive summary
   ## Key findings
   ## Recommendations
   ```

   ```md
   ## Quick Example 2: Commit message format
   **Example 1:**
   Input: Added user authentication with JWT tokens
   Output: feat(auth): implement JWT-based authentication
   ```

#### **2.3 When the SKILL.md and its resources are completely drafted, re-read once with fresh eyes for improvements. Then proceed to Phase 3 Validation

---

### Phase 3: Validate as you go

**Scope-lock** :
- Polish how the skill works, don't change what it does. No new capabilities, no new dependencies.
- Every finding must cite the specific line number. No vague claims.
- Don't apply changes without user confirmation and git save.
- Keep wip folder a living doc for future review

**LOOP until user approves:**

   #### 3.1 Static Validation
   Run `scripts/quick_validate.py <skill-dir>`. Report every FAIL item with proposed fix. Apply only after user confirmation.

   #### 3.2 Verification with Evidence
   Work through the checklist. Fill Evidence for each item — quote specific content, not opinions. Report gaps and proposed fixes; apply only after user confirmation.

   | Check | Evidence |
   |-------|----------|
   | [ ] Instructions are concise and actionable? | |
   | [ ] Every section justifies its inclusion? | |
   | [ ] No duplicated content between body and references? | |
   | [ ] Standard section elements all present? | |
   | [ ] Workflow detail guides followed? | |
   | [ ] Input / output formats properly defined? | |
   | [ ] Re-read with fresh eyes? | |


   If script fixes were applied, go back to 3.1.
   If checklist gaps were fixed, re-check only those items.

   #### 3.3 Approval Gate
   When 3.1 has zero FAILs and 3.2 Evidence is all filled:
   → Ask user whether fine with this phase. Show and save a summary to `<skill-name>/.wip/validation-N-summary.md` .
   → If new gotchas were discovered during validation, propose them for the Critical Gotchas table.
   → On user approval: exit Phase 3.


### Phase 4 (Optional): Package a Skill when asked

When jumping directly here (skipping Phase 3), package_skill.py auto-runs validation as a gate. 

```bash
scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

Reports any FAIL items before packaging. On success, creates a `<skill-name>.skill` file.


## Meta Evolution Check

**Scope Rules** — Evolution records belong to the skill that produced the insight,
not necessarily the skill that was used to create it. Before recording, determine scope:

1. **Process-level issues** — (e.g., skipped steps, unclear instructions in zao-skill itself,
   agent misinterpreted zao-skill's directives)
   → update **zao-skill's** `references/skill-evolution.md` (this file).

2. **Implementation-level issues** — (e.g., code bugs, algorithm flaws, format problems in
   a skill zao-skill just helped create)
   → update **the target skill's** `references/skill-evolution.md` (create it if missing).

3. **Cross-cutting issues** — (e.g., zao-skill wasn't explicit enough about X,
   leading to target-skill error Y)
   → update **both**, with a cross-reference note.

--- 

**Trigger**: Agent self-checks after each run: 
 did it produce a repeatable fix or a meaningful improvement?  
- If uneventful, skip. 
- If yes → follow `references/skill-evolution.md` to maintain following tables.

### Critical Gotchas
| ID | Issue / Symptom | Fix |
|----|----------------|-----|
| G01 | Memory reliance — acted on stale context, not current file | Re-read target file before any edit |
| G02 | Closure seeking — assumed workflow complete after one sub-task | Review step checklist, don't skip |
| G03 | Cognitive laziness — skipped reference files, relied on main doc alone | Follow "see references/..." instructions, no spot-check |

### Success Patterns
| Date | Change | Context | Result |
|------|--------|---------|--------|
| -- | -- | -- | -- |


## Exit Verification

- Meta Evolution Check done? → any insights recorded?
- Critical Directives: re-read the Pre-Step Rationalization Bias Check — skipped any steps?
- Phase 3 rules still apply: scope-lock, cite line numbers, user confirmation


