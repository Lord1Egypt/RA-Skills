---
name: vibe-coding-blueprint
description: "A document-driven AI programming methodology. Use when: (1) starting a new code project, (2) adding a new feature module, (3) debugging a bug, (4) code becomes messy and needs refactoring, (5) user mentions vibe coding, document-driven, small-step iteration. Core: plan-first, iterate in small steps, documents as memory, human in command."
---

# Vibe Coding Blueprint

A document-driven AI programming methodology. AI is like a "highly capable but occasionally careless new hire." Your role is **Architect and Decision Maker** — not overseer.

- AI handles high-speed code output
- You handle judgment, decisions, and root cause diagnosis
- **The steering wheel stays in your hands**

---

## Core Philosophy

AI code generation is powerful but fragile. Without structure, it produces code that works once but becomes unmaintainable over time. This methodology solves that through **documents as memory** — a self-referential documentation system that lets AI resume from any state without losing context.

---

## The Workflow

### Phase 0: Check Project Documentation Status

**Important:** At the start of every conversation, check if the project already has documentation:

1. Check if `docs/README.md` exists
2. Check if `docs/ARCHITECTURE.md` exists
3. Check if `docs/PROJECT_STRUCTURE.md` exists
4. Check if main source folders have `FOLDER.md`

**If documentation exists:**
```
Project documentation detected:
- docs/README.md
- docs/ARCHITECTURE.md
- docs/PROJECT_STRUCTURE.md
- [list of FOLDER.md files]

I will read these docs first to understand the project context before starting work.
```

**If no documentation:**
```
No documentation structure found.
Please choose:
A) Initialize documentation (recommended) — generate a complete documentation structure
B) Skip initialization — start working directly without docs

Choose [A/B]:
```

---

### Phase 1: Blueprint — Design the Architecture First

**Goal:** Think through the entire system architecture in your head, then output it to a formal document.

**Steps:**
1. Define the core problem the system solves
2. Break down core modules
3. Map data flow and key dependencies
4. Output to `docs/ARCHITECTURE.md`

**Output file:** `docs/ARCHITECTURE.md`

---

### Phase 2: Establish Fractal Documentation Structure

**Goal:** Build a self-referential documentation system. AI can return to any prior state and continue working.

#### Three-Layer Documentation System

**Layer 1 — Root documentation**
```
docs/
├── README.md              # Root doc, declares update mechanism
├── ARCHITECTURE.md       # System architecture overview
├── PROJECT_STRUCTURE.md   # Project structure guide (quick navigation)
└── superpowers/
    └── DAILY.md           # Daily change log
```

**Layer 2 — Folder-level docs** (one `FOLDER.md` per folder, ≤3 lines)
```markdown
# [Folder Name] Architecture

**Role:** [One-line description]
**Contains:** [file name] - [function], [file name] - [function]

> ⚠️ If this folder changes, update this document
```

**Layer 3 — Code file header (3 lines)**
```typescript
// input:  [what this file depends on externally]
// output: [what this file provides to others]
// pos:    [this file's role in the local system]
// ⚠️ When this file is updated, update its header and the parent FOLDER.md
```

**Self-reference mechanism:** Local changes propagate to global; global changes propagate to local. When any file changes, it automatically triggers a cascade of documentation sync.

---

### Phase 3: Develop Module by Module (Core Loop)

Each feature module follows these steps:

#### Step 1: Design the Plan First (Plan-Before-Code)

**Do not write code immediately.** Have AI output the technical implementation plan first, then you review and adjust.

Prompt template:
```
Before implementing [module name], please output the technical implementation plan:
1. Data model design (table schema or type definitions)
2. Core interfaces (function names, params, return values)
3. Dependencies on other modules
4. Key implementation details
5. Potential pitfalls

I will review and confirm before you start coding.
```

**Your (human) responsibilities:**
- Review if the plan is sound
- Adjust permission and boundary design
- Confirm tech stack choices
- Add missing edge cases

#### Step 2: Break Into Small Tasks

Split the module into **small, independently completable tasks**.

Each small task includes:
- ✅ Clear objective
- ✅ Technical approach
- ✅ Implementation steps
- ✅ Verification method

#### Step 3: Implement One Small Task at a Time

**Order:** Foundation → Business logic → UI layer

After completing each small task, **immediately:**
1. Update the code file's header comments
2. Update the parent folder's `FOLDER.md`
3. Run verification (unit test, demo page, or manual test)

**Prompt template** (after verification):
```
Verification passed. Now please:
1. Update [filename] header comments (if implementation changed)
2. Update docs/[folder]/FOLDER.md (if interfaces changed)
3. If there are cross-folder dependencies, sync related docs
```

#### Step 4: End-to-End Integration

After all modules are complete, run end-to-end tests.

---

### Phase 4: Debugging (Human-in-Command Moment)

**Most important principle:** When the same problem remains unfixed after 2–3 iterations, **stop immediately**. This signals the model is trapped in a wrong framework.

#### Debugging Steps

**Step 1: Recognize danger signals**
- Model has modified the same issue 2–3+ times without resolution
- Fixing one thing breaks another (patch on patch)
- Code is getting messier, not cleaner

**Step 2: Human diagnoses root cause**
- Read error messages, but don't stop at surface level
- Use logs, breakpoints, and code tracing to find the real cause
- Ask: Which module did the problem occur in? Why did it happen? What is the root cause?

**Step 3: Tell the model the root cause explicitly**

❌ Don't say: `There's a bug here, please fix it`
✅ Say: `Your previous assumption was wrong. The real problem is: [specific description of root cause, including why]. Based on this understanding, please re-implement.`

**Step 4: Let the model re-generate based on correct understanding**

---

### Phase 5: Iteration

| Scenario | Entry |
|---------|-------|
| New feature | Back to Step 1 — treat it as a mini project; note existing stack in "System background" |
| Performance/UX issue | Debugging mode — describe problem + paste relevant code |
| Messy code | Redesign module boundaries, then start adding features |

---

## Human-AI Role Table

| Phase | Your Role | AI's Role |
|-------|-----------|-----------|
| Planning | Architecture decisions, permission boundaries, tech choices | Plan review, feasibility analysis, detail supplementation |
| Code | Plan review, code review, key troubleshooting | Heavy lifting (CRUD, interface docs, field sync) |
| Root cause | Root cause analysis, problem diagnosis | Fix based on your guidance |
| Testing | Test design, edge case supplementation | Test script generation, demo pages |

---

## Common AI Pitfalls & Solutions

### 1. API Hallucination
AI invents APIs, library functions, or interfaces that don't exist.
**Solution:** Emphasize in prompts "use only APIs from official documentation." Verify against official docs when needed.

### 2. Repeated Patching on Wrong Assumptions
AI keeps modifying code based on a wrong foundational assumption, making things worse.
**Solution:** Diagnose the root cause yourself, then explicitly tell AI what the wrong assumption was.

### 3. Over-Engineering
AI generates excessive design patterns, factory functions, and decorators.
**Solution:** Delete freely during code review. Keep code simple.

### 4. Missing Edge Cases
AI only implements the happy path; null checks, exceptions, and concurrency are neglected.
**Solution:** Enumerate edge cases in prompts upfront, or supplement during the testing phase.

---

## Prompt Template Library

### Start a New Project
```
I want to start a new project: [project description]
Please help me output the project architecture doc first:
1. Core module breakdown
2. Data flow relationships
3. Tech stack recommendations

I will confirm before you set up documentation structure and start coding.
```

### Add a New Feature
```
I want to add [new feature] to [existing module].
Please output the technical implementation plan first.
I will confirm before you start coding.
```

### Debugging Request
```
I'm encountering a problem:
- Symptom: [description]
- Expected: [expected behavior]
- Actual: [actual behavior]

I've tried: [attempts so far]

Before fixing, please analyze possible causes. I'll tell you the root cause and then we'll fix it.
```

### Sync Docs After Update
```
[module name] is complete. Please sync:
1. Header comments in [filename] (if interfaces changed)
2. docs/[folder]/FOLDER.md
3. docs/ARCHITECTURE.md (if significant changes)
4. docs/PROJECT_STRUCTURE.md (if new modules added)
```

### Initialize Documentation for Existing Project
```
This is an existing project without documentation. Please initialize its documentation structure.
```
> Note: Initialization starts by exploring the actual project structure, not assuming a specific layout (like src/), then generates documentation matched to the real structure.

---

## Efficiency Target

If this methodology is followed strictly, content you genuinely need to write yourself should be < 5%:
- Minor wording adjustments
- Root cause analysis and problem diagnosis
- Boundary case decisions
- Code review and architecture adjustments

AI handles the remaining 95%: heavy lifting, repetitive work, high-speed code generation.
