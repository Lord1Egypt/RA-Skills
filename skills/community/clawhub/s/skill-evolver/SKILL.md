---
name: skill-evolver
description: |
  A complete skill lifecycle manager for discovering, orchestrating, fusing, and evolving skills.

  Helps decide which skills to use, how to compose or fuse them, and whether to materialize
  a successful workflow into a new reusable skill.

  Trigger when:
  - User asks how to choose or combine skills
  - No single skill is sufficient and orchestration is needed
  - A solved workflow may need to be preserved as a new skill
  - Multiple skills need to be fused into one

  Do not trigger when:
  - User explicitly requests one specific skill
  - Native Claude ability is obviously sufficient
---

# Skill Evolver

Solve first. Materialize later.

## Workflow

### Phase 0: Setup Output Directory

Create a timestamped output directory for this session:
```bash
# Format: output/MM-DD-<feature-slug>/
# Example: output/03-09-pdf-translate/
mkdir -p "output/$(date +%m-%d)-<feature-slug>"
```

> **Tip**: Use a short slug derived from the task (e.g., `pdf-translate`, `data-export`, `api-integration`)

Store the output path for subsequent phases:
```
OUTPUT_DIR=output/<created-directory>
```

### Phase 1: Intent Analysis
Analyze the user task and output `${OUTPUT_DIR}/01-intent.md`.
See template: [references/templates/01-intent.md](references/templates/01-intent.md)

### Phase 2: Skill Search

Follow the complete skill search workflow:
→ [references/skill-search.md](references/skill-search.md)

This workflow covers:
- CLI prerequisites and installation
- Local + Registry (dual-track) search
- Skill selection checkpoint
- Installation and verification
- Security audit

**Output files:**
- `${OUTPUT_DIR}/02-candidates.md` - Merged search results
- `${OUTPUT_DIR}/02-verify.md` - Installation verification (if installed)
- `${OUTPUT_DIR}/02-audit.md` - Security audit report (if installed)

### Phase 3: Deep Inspection
For each candidate skill, perform deep analysis:

Follow the workflow: [references/skill-inspector.md](references/skill-inspector.md)

Output: `${OUTPUT_DIR}/03-inspection.md`

### Checkpoint: Approach Decision

After inspection, evaluate whether skills can solve the task:

**LLM evaluates:**
- Do skill capabilities match task requirements?
- Is modification needed?
- Is fusion beneficial?

**LLM Recommendation:**
- **Orchestration** (skills match well, no major modification)
- **Fusion** (skills partially match, combining creates new value)
- **Native** (no suitable skills found)

Options for user:
- **A**: Orchestration (LLM recommended)
- **B**: Skill Fusion (enter coding mode)
- **C**: Use native abilities instead
- **D**: Re-analyze (return to Phase 3)

### Phase 3.5: Skill Fusion (Conditional)

Only if approach is **Fusion**

Follow the complete skill fusion workflow:
→ [references/skill-fusion.md](references/skill-fusion.md)

This workflow covers:
- Fusion spec design
- Invoke skill-creator
- Audit fused skill

**Output files:**
- `${OUTPUT_DIR}/03-fusion-spec.md` - Fusion specification
- `${OUTPUT_DIR}/03-fusion-audit.md` - Security audit (if fusion)

### Phase 4: Orchestration
Design execution plan and output `${OUTPUT_DIR}/04-orchestration.md`.
See template: [references/templates/04-orchestration.md](references/templates/04-orchestration.md)

### Checkpoint: Plan Confirmation

Use `AskUserQuestion` tool (or similar tool to Human-in-the-Loop) to confirm plan:
- **A**: Proceed with this plan
- **B**: Modify the plan
- **C**: Show alternatives
- **D**: Additional requirements (then revise)

### Phase 5: Execution
Execute the plan. For each step:
- Native: use your own reasoning
- Skill: invoke the skill with appropriate input

### Checkpoint: Materialization Decision

Use `AskUserQuestion` tool (or similar tool to Human-in-the-Loop) to ask about preservation:
- **A**: Yes, create a new skill (invoke `skill-creator`)
- **B**: No, this was one-time
- **C**: Save as draft for later review
- **D**: Additional requirements (then adjust scope)

## Principles

```
Priority: native > orchestration > temporary > persistent

- Prefer native for simple tasks
- Prefer orchestration when existing skills can solve it
- Materialize only after validation + proven reuse value
- Always provide option [D] for additional input
- Re-optimize when user provides new information
```
