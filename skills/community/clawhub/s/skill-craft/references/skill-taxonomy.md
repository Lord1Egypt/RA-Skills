# Skill Taxonomy Reference

> Evidence-based classification system for AI agent skills.
> Sources: 10 academic papers (CoALA, PromptPrism, etc.) + 5 engineering platforms (Claude Code, Cursor, Superpowers, OpenClaw, Windsurf).

---

## Quick Classification Decision Tree

When classifying a skill, ask these questions in order:

1. **Is it about skills themselves?** (create/optimize/discover skills) → META
2. **Does it wrap an external tool/service?** (database, browser, calculator) → TOOL
3. **Does it enforce a proven method?** (TDD, debugging, verification) → METH
4. **Does it define execution order/phases?** (brainstorming, planning, execution) → PROC
5. **Does it coordinate multiple agents/tasks?** (parallel dispatch, sub-agents) → ORCH
6. **Does it verify/audit work quality?** (code review, completion checks) → QA
7. **Does it provide domain expertise?** (UI design, mobile patterns, framework docs) → KNOW
8. **Does it generate structured output?** (reports, wikis, documentation) → DOC
9. **Does it guide creative output?** (prompt refinement, design ideation) → GEN

**Priority rules when multiple types apply:**
- Safety/Quality first: QA > METH > PROC
- Process before execution: PROC (brainstorming → plans) > METH (TDD)
- Meta skills last: META only on explicit request
- Tools on demand: TOOL only when specific capability is needed
- Domain by context: KNOW only when relevant domain is detected

---

## 9 Skill Types

### PROC — Process Control

- **Definition**: Defines what order tasks should be executed in and which phases they pass through.
- **Design Template**:
  ```markdown
  ## Overview
  [One sentence: what this process does]

  ## When to Use
  - [Scenario 1]
  - [Scenario 2]

  ## Process Flow
  [Numbered steps or Mermaid diagram]

  ## Checklist
  1. [Step 1]
  2. [Step 2]

  ## Decision Points
  [Key branches and conditions]

  ## Transition
  [What to do after the process completes]
  ```
- **Key Elements**: Clear phase boundaries (start → middle → end); completion criteria per phase; decision nodes with branch logic; transition points to other skills; HARD-GATE to prevent skipping steps.
- **Common Pitfalls**: Steps too vague ("analyze code" should be specific sub-steps); no completion criteria; no decision points (every real flow has branches).
- **Examples**: brainstorming, writing-plans, executing-plans, finishing-a-development-branch

---

### METH — Methodology

- **Definition**: Provides proven, reusable methods and principles for engineering activities.
- **Design Template**:
  ```markdown
  ## The Iron Law
  [Core principle in a code block — inviolable]

  ## When to Use
  **Always:**
  - [Mandatory scenarios]
  **Exceptions (ask your human partner):**
  - [Exception scenarios]

  ## Process
  1. [Step 1]
  2. [Step 2]

  ## Anti-Patterns
  | Wrong | Right | Why |
  |-------|-------|-----|

  ## Verification
  [How to verify the method was followed correctly]
  ```
- **Key Elements**: Iron Law in a code block (emotionally salient, impossible to miss); explicit "Always" and "Exceptions"; Anti-Pattern table (wrong vs right + reason); verification steps; positive constraints ("do X" not "don't do Y").
- **Common Pitfalls**: Too many rules (agent selectively ignores); excessive negative constraints (positive constraints are empirically more reliable per Inverse IFEval); no exceptions (causes rigidity); "this is too simple" fallacy (simple tasks still need methodology).
- **Examples**: test-driven-development, systematic-debugging, verification-before-completion, post-dev-verification

---

### TOOL — Tool Integration

- **Definition**: Wraps an external tool, API, or CLI into a reusable agent capability.
- **Design Template**:
  ```markdown
  ## Prerequisites
  [Installation and configuration requirements]

  ## Decision Guide
  | Need | Method | Example |
  |------|--------|---------|

  ## Usage
  ### Basic
  [Simplest usage]
  ### Advanced
  [Complex scenarios]

  ## Error Handling
  [Common errors and solutions]

  ## Verification
  [How to verify the tool works correctly]
  ```
- **Key Elements**: Prerequisites check (don't assume installed); Decision Guide table (what need → what method); progressive usage (simple → complex); error handling guide; script wrappers (deterministic ops, no context consumed).
- **Common Pitfalls**: Assuming tool is pre-installed; only one usage path (missing Decision Guide); incomplete error handling (agent doesn't know what to do on script failure).
- **Examples**: web-access, calculator, db-toolkit, context7-docs-lookup

---

### KNOW — Domain Knowledge

- **Definition**: Provides specialized expertise, conventions, and best practices for a specific domain.
- **Design Template**:
  ```markdown
  ## Configuration
  [Baseline configuration parameters]

  ## Rules
  [Specific, quantifiable rules]

  ## Anti-Patterns / Bias Corrections
  [LLM biases and how to counter them]

  ## Examples
  ### Good
  [Correct approach]
  ### Bad
  [Incorrect approach]

  ## References
  - **Detailed spec**: See [file.md](references/file.md) when [trigger condition]
  ```
- **Key Elements**: Quantifiable rules ("Max 1 Accent Color. Saturation < 80%"); Anti-Patterns for LLM bias correction; Good/Bad contrast examples; progressive loading (core rules in SKILL.md, details in references/); baseline config parameters.
- **Common Pitfalls**: Rules too vague ("write clean code" → needs specific, measurable rules); SKILL.md too long (move details to references/); no bias correction (LLM statistical bias causes generic output).
- **Examples**: design-taste-frontend, mobile-design, openclaw-plugin-dev

---

### GEN — Creative/Generative

- **Definition**: Guides creative output by providing quality standards and inspiration without rigid constraints.
- **Design Template**:
  ```markdown
  ## Principles
  [Creative philosophy and guiding principles]

  ## Quality Bar
  [Quality standards and evaluation criteria]

  ## Freedom Calibration
  [Freedom settings and creative boundaries]

  ## Examples
  [High-quality reference examples]

  ## Process
  1. [Understand requirements]
  2. [Explore approaches]
  3. [Generate output]
  4. [Self-review and refine]
  ```
- **Key Elements**: Principles over rules (High Freedom); quality bar (example-driven standards); freedom calibration (explicit creative boundaries); self-review step (evaluate creative output against requirements).
- **Common Pitfalls**: Too many rules constraining creative space; no quality bar (output quality inconsistent); no self-review (output may drift from requirements).
- **Examples**: prompt-refiner

---

### DOC — Document Generation

- **Definition**: Generates structured documents, reports, or analyses with consistent formatting.
- **Design Template**:
  ```markdown
  ## Report Structure
  [Output document structure specification]

  ## Sections
  ### Section 1: [Title and content requirements]
  ### Section 2: [Title and content requirements]

  ## Output Format
  [Format requirements: Markdown, Mermaid, tables, etc.]

  ## Verification
  [Document completeness checklist]
  ```
- **Key Elements**: Fixed output structure; per-section content requirements; format specification (Markdown, Mermaid, tables); completeness verification checklist.
- **Common Pitfalls**: Unfixed output structure (format inconsistency); no verification step (documents may be incomplete).
- **Examples**: repowiki, project-docs-generator

---

### ORCH — Orchestration

- **Definition**: Manages collaboration between multiple agents, tasks, or resources.
- **Design Template**:
  ```markdown
  ## When to Use
  [Decision flowchart: under what conditions]

  ## Dispatch Strategy
  [How to split and assign tasks]

  ## Sub-agent Prompt Template
  [Template for sub-agent prompts]

  ## Result Aggregation
  [How to collect and merge results]

  ## Error Handling
  [Strategy when sub-tasks fail]
  ```
- **Key Elements**: Decision flowchart (dot format); sub-agent prompt template; result aggregation strategy; error handling and retry logic.
- **Common Pitfalls**: Sub-tasks with dependencies are parallelized; sub-agent prompts lack necessary context; no error handling (one failure cascades to all).
- **Examples**: dispatching-parallel-agents, subagent-driven-development, using-git-worktrees

---

### META — Meta-Skill

- **Definition**: Skills about skills — managing, creating, discovering, and optimizing the skill system itself.
- **Design Template**:
  ```markdown
  ## Core Principle
  [The meta-skill's foundational principle]

  ## Two Modes of Operation
  **MODE A:** [Description]
  **MODE B:** [Description]

  ## Framework
  [Underlying framework or taxonomy the meta-skill operates on]

  ## Anti-Patterns
  [Common errors when using the meta-skill]
  ```
- **Key Elements**: Clear meta-level positioning (skill about skills); multiple operation modes; underlying framework or taxonomy; recursion safety (must not infinitely invoke itself).
- **Common Pitfalls**: Infinite recursion (meta-skill invoking itself); blurred responsibility with managed skills.
- **Examples**: using-superpowers, skill-craft, writing-skills, prompt-refiner

---

### QA — Quality Assurance

- **Definition**: Verifies, audits, and ensures work quality through evidence-based checks.
- **Design Template**:
  ```markdown
  ## The Iron Law
  [Inviolable verification principle: evidence before assertions]

  ## When to Use
  **Mandatory:** [Must-use scenarios]
  **Optional:** [Recommended scenarios]

  ## Verification Steps
  1. [Step 1]
  2. [Step 2]

  ## Failure Protocol
  [What to do when verification fails]

  ## Evidence Requirements
  [What counts as "passing"]
  ```
- **Key Elements**: Iron Law (evidence before assertions always); explicit verification steps; failure protocol; evidence requirements (what proves quality).
- **Common Pitfalls**: Incomplete verification commands (only partial tests run); stale evidence (using cached old results); no failure handling (don't know what to do when checks fail).
- **Examples**: requesting-code-review, receiving-code-review, post-dev-verification, doc-sync-all

---

## Skill Type Combination Patterns

Common tasks and recommended skill combinations:

| Task | Recommended Skills | Order |
|------|-------------------|-------|
| New feature | brainstorming → writing-plans → TDD → verification → code-review | Sequential |
| Bug fix | systematic-debugging → TDD → verification | Sequential |
| Large refactor | brainstorming → writing-plans → parallel-agents → verification | Mixed |
| Frontend work | brainstorming → design-taste-frontend → TDD → verification | Sequential |
| Skill development | skill-craft (CREATE) → skill-craft (OPTIMIZE) | Sequential |
| Research task | web-access + calculator + prompt-refiner | On-demand |
| Documentation | repowiki / project-docs-generator | Single |
| Multi-task parallel | dispatching-parallel-agents → per-task skills → verification | Fan-out/fan-in |
| PR submission | verification → requesting-code-review → finishing-a-branch | Sequential |

---

## Eight Classification Dimensions

Each skill can be tagged: `TYPE:GRANULARITY:AUTONOMY:FREEDOM`

1. **Type** (PROC/METH/TOOL/KNOW/GEN/DOC/ORCH/META/QA) — Core classification of what the skill does.

2. **Granularity** — Atomic (single function, e.g. calculator) / Molecular (multi-step flow, e.g. systematic-debugging) / Composite (composable capabilities, e.g. brainstorming).

3. **Autonomy** — Guided (requires human step-by-step confirmation, e.g. brainstorming) / Supervised (autonomous execution with key-node confirmation, e.g. executing-plans) / Autonomous (fully independent, e.g. verification-before-completion).

4. **Freedom Level** — Low (numbered steps + scripts, strict constraints → best for METH/TOOL) / Medium (preference patterns + parameters → best for PROC/DOC) / High (principles + examples → best for GEN/KNOW).

5. **Loading Level** — L1 (name + description, always loaded, ~100 tokens) / L2 (SKILL.md body, loaded on trigger, <5k tokens) / L3 (references/scripts/assets, loaded on demand).

6. **Statefulness** — Stateless (each invocation independent, e.g. calculator) / Session-state (persists within conversation, e.g. brainstorming) / Persistent (persists across sessions).

7. **Trigger Mode** — Keyword (description keyword match) / Context (task context inference) / Explicit (user explicitly requests) / Always (loaded every conversation, e.g. using-superpowers).

8. **Dependency Complexity** — Standalone (no external deps) / External-Tool (requires external tool/service) / Multi-Resource (requires multiple scripts/references/templates).

**Tag examples:**
- `systematic-debugging` → `METH:Molecular:Supervised:Low`
- `brainstorming` → `PROC:Composite:Guided:Medium`
- `calculator` → `TOOL:Atomic:Autonomous:Low`
- `design-taste-frontend` → `KNOW:Molecular:Supervised:High`
- `skill-craft` → `META:Composite:Guided:Medium`

---

## Key Design Principles

These are empirically supported by the research:

| Principle | Evidence | Impact |
|-----------|----------|--------|
| Keep SKILL.md under 500 lines | Claude Code Issue #2544 (39👍) | Longer skills → lower compliance |
| Use positive constraints ("do X") | Inverse IFEval (ByteDance, 2025) | More reliable than negative ("don't do Y") |
| Good/Bad examples | Cursor official data | ~3x more effective than rules alone |
| 1-shot examples | ACL 2025 | Best flexibility/structure balance |
| Decompose constraints | Constraint Decomposition (2025) | 41.2% → 73.8% accuracy |
| Format + content optimization | CFPO (Fudan/Microsoft, 2025) | +5~38% improvement |
| Iron Law in code blocks | Superpowers practice | Emotionally salient, hard to miss |
| Progressive disclosure (L1→L2→L3) | Claude Code architecture | Tokens are a shared resource |

---

## Sources

### Academic Papers (10)
1. Sumers et al., "Cognitive Architectures for Language Agents" (CoALA), ICLR 2024 Oral
2. White et al., "A Prompt Pattern Catalog to Enhance Prompt Engineering", 2023 (600+ citations)
3. Jeoung et al., "PromptPrism: A Linguistically-Inspired Taxonomy for Prompts", EACL 2026
4. Joyce & Maheshwari, "A Design-Driven Taxonomy of AI Agentic Patterns", IEEE ICAI 2025
5. Fagbohun et al., "An Empirical Categorization of Prompting Techniques", 2024
6. Buyya et al., "Agentic AI: Architectures, Taxonomies, and Evaluation", 2026
7. Li et al., "Towards Secure Agent Skills: Architecture, Threat Taxonomy", 2026
8. Piskala, "Agent, Sub-Agent, Skill, or Tool?", Authorea 2026
9. Gao et al., "A Taxonomy for Human-LLM Interaction Modes", 2025
10. Ng & Fulford, "ChatGPT Prompt Engineering for Developers", DeepLearning.AI 2023

### Engineering Platforms (5)
1. Anthropic Claude Code — Agent Skills Overview & Authoring Best Practices (2025)
2. Cursor — Rules Documentation (2025-2026)
3. obra/superpowers — Five-type classification + nine-dimension optimization framework
4. OpenClaw — Plugin system (Hook/Tool/Provider/Channel)
5. Windsurf — Agent skill patterns

---

*Condensed from the full 1231-line research report. See `/home/leonardo123/docs/superpowers/research/phase3/skill-taxonomy.md` for complete analysis.*
