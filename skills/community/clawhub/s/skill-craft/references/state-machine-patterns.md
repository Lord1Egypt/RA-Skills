# State Machine Patterns for Skills

> Design patterns for adding state management to AI agent skills.
> Sources: OpenSpec (DAG + artifact graph), LangGraph (StateGraph + checkpoint), Source Code Agent (arXiv:2508.02721), Compiled AI (arXiv:2604.05150), Claude Code Hooks (25+ events), MetaGPT (Code=SOP), smolagents (Code-as-Action).

## When to Add State Management

| Condition | Needs State? | Why |
|---|---|---|
| Multi-step workflow with step dependencies | YES | Step B needs output from Step A |
| Output feeds into next invocation | YES | Resume from checkpoint |
| Single-shot tool call | NO | Stateless is simpler |
| Free-form exploration / brainstorming | NO | No fixed path to track |
| Verification reads current state | Light | Reads state but doesn't advance it |

**Key insight:** Research (arXiv:2511.07585) shows large models (GPT-OSS-120B) have only **12.5% output consistency** across runs. Deterministic state checks (file existence, script output) are **8x more reliable** than LLM self-assessment. Small models (8B) at T=0.0 achieve 100% consistency.

## 4 State Patterns (Simple to Complex)

### Pattern 1: File Existence Checks (Simplest)

**Concept:** Each step generates a file. File exists = step done. Zero config, Git-friendly, human-readable.

**How it works:**
```javascript
// OpenSpec's actual implementation (~15 lines)
function isArtifactComplete(generates, changeDir) {
    if (isGlobPattern(generates)) {
        return hasGlobMatches(path.join(changeDir, generates));
    }
    return fs.existsSync(path.join(changeDir, generates));
}
```

**Workflow example:**
```markdown
## Workflow
1. Research -> writes `output/research.md`
2. Plan -> requires `output/research.md` -> writes `output/plan.md`
3. Implement -> requires `output/plan.md` -> writes code files
4. Verify -> requires implementation -> runs tests
```

**SKILL.md integration:**
```markdown
## State Detection
Before starting, check which phase to resume:
- If `output/research.md` exists AND `output/plan.md` does NOT -> start at Plan
- If `output/plan.md` exists AND no code files -> start at Implement
- If code exists -> start at Verify
```

**Advantages:** Zero infrastructure, Git-trackable, LLM can read/write directly.
**Disadvantages:** No metadata (timestamps, error info), glob patterns need care.

### Pattern 2: Checkbox Tracking (Medium)

**Concept:** Markdown checkboxes track sub-task progress. LLM reads checkboxes to know what's done, marks them complete as it progresses.

**OpenSpec's implementation (Apply phase):**
```javascript
// State detection from tasks.md checkboxes
if (remaining === 0 && total > 0) state = 'all_done';
else if (total === 0) state = 'blocked';  // no tasks defined
else state = 'ready';                       // work to do
```

**Example:**
```markdown
## Tasks
- [x] 1.1 Extract fields from schema
- [x] 1.2 Validate against rules
- [ ] 2.1 Generate output report
- [ ] 2.2 Run integration tests
```

**SKILL.md integration:**
```markdown
## Progress Tracking
1. Read `tasks.md` to find unchecked items
2. Work through the next unchecked task
3. Mark it complete: `- [x]` when done
4. Repeat until all items are checked
5. When all checked -> move to next phase
```

**Advantages:** Human-readable, Git-diffable, natural LLM interaction.
**Disadvantages:** No parallel tracking, checkbox parsing can be fragile.

### Pattern 3: YAML State File (Complex)

**Concept:** Explicit YAML file records workflow state, metadata, and context. Supports richer information than file existence alone.

**Example:**
```yaml
# .skill-state.yaml
phase: design
completed: [research, plan]
blocked: [implement]
metadata:
  started: 2026-04-14
  last_updated: 2026-04-14T10:30:00
  iterations: 2
  errors: []
```

**State machine definition (optional):**
```yaml
state_machine:
  initial: brainstorming
  states:
    - name: brainstorming
      transitions: [planning, direct_response]
    - name: planning
      transitions: [executing, cancelled]
    - name: executing
      transitions: [verifying, failed]
    - name: verifying
      transitions: [complete, executing]  # loop back for fixes
    - name: complete
      transitions: []  # terminal
```

**Advantages:** Rich metadata, supports iteration counts and error history.
**Disadvantages:** Extra file to manage, must stay in sync with reality.

### Pattern 4: Schema-Driven DAG (Most Complete)

**Concept:** YAML defines artifact dependency graph. Script detects state via topological sort. Prevents skipping steps, supports parallel-ready artifacts.

**Full schema example (OpenSpec pattern):**
```yaml
name: my-workflow
version: 1
artifacts:
  - id: research
    generates: research.md
    template: templates/research.md
    instruction: |
      Research the topic and document findings.
      Include: Background, Current State, Key Findings.
    requires: []
  - id: plan
    generates: plan.md
    requires: [research]
  - id: implement
    generates: "src/**/*.py"
    requires: [plan]
  - id: verify
    generates: verification-report.md
    requires: [implement]
apply:
  requires: [verify]
  tracks: verification-report.md
```

**Three-state model per artifact:**

| State | Meaning | Condition |
|---|---|---|
| `done` | Completed | `generates` file exists in change dir |
| `ready` | Can create | All `requires` are done, self not done |
| `blocked` | Waiting | At least one `requires` not done |

**Parallel-ready detection:** If two artifacts share the same dependency but don't depend on each other, both become `ready` simultaneously (e.g., `specs` and `design` both depend only on `proposal`).

**Advantages:** Prevents step-skipping, supports parallel work, fully declarative.
**Disadvantages:** Requires schema file, more complex setup. OpenSpec core is ~500 lines.

## Generate-Validate-Fix Loop

**Core pattern from MindStudio + Compiled AI research:**

```
Agent generates -> Script validates -> If fail -> Agent fixes (max 3 rounds) -> If still fail -> escalate
```

**Research evidence:**
- Compiled AI (arXiv:2604.05150): 96% task completion with **zero runtime tokens** after compilation
- MindStudio: 3-5 iteration limit is the production standard
- Source Code Agent: Blueprint-First beats free-form by **+10.1 pp Pass@1**

**SKILL.md integration:**
```markdown
## Verification Loop
1. Generate output following the workflow
2. Run `scripts/validate.sh <output>` to check format/schema/tests
3. If validation passes -> done, mark task complete
4. If validation fails:
   a. Read the exact error message
   b. Fix ONLY the specific issues reported
   c. Re-run validation (go to step 2)
5. After 3 failed attempts -> report to user with partial results and error log
```

**Three-level validation hierarchy (from OpenSpec):**

| Level | When | What | Tool |
|---|---|---|---|
| Structure | Init / transition | Files exist, schema valid, no cycles | Zod/JSON Schema |
| Content | After artifact creation | Required sections present, format correct | Regex / parser / script |
| Semantic | After all artifacts | Implementation matches spec, no missing requirements | Code search / tests / LLM |

## Script Integration Patterns

### The Golden Rule

> **If a step CAN be a script, it SHOULD be a script.**

Compiled AI proves that compiling LLM output into deterministic code achieves **57x cost reduction** at scale (1000 transactions). smolagents' Code-as-Action reduces steps by **30%** vs ReAct.

### Deterministic vs Probabilistic Steps

| Step Type | Implementation | Reliability | Token Cost |
|---|---|---|---|
| Format checking | `scripts/validate.py` | 100% | 0 |
| Schema validation | `scripts/check_schema.py` | 100% | 0 |
| Code formatting | `prettier --write` | 100% | 0 |
| Dependency checking | `scripts/check_deps.sh` | 100% | 0 |
| Test execution | `pytest / npm test` | 100% | 0 |
| Creative decisions | LLM judgment | ~50-87% | High |
| State assessment | File existence check | 100% | 0 |
| State assessment | LLM self-report | ~12.5% | High |

### Script + SKILL.md Integration Modes

**Mode A: Script as Validation Gate**
```markdown
## Verification
1. Run `scripts/validate.sh <output>` to check format compliance
2. If exit code 0 -> proceed to next step
3. If exit code != 0 -> read stderr, diagnose, fix, re-validate
```

**Mode B: Script as Core Execution (Blueprint-First)**
```markdown
## Workflow
1. Prepare: `scripts/prepare.py --input <source>` -> generates working files
2. Transform: LLM processes each file following template
3. Verify: `scripts/validate.py --config references/schema.yaml <output>`
4. Format: `scripts/format.sh <output>` -> final cleanup
```

**Mode C: Script as Environment Check**
```markdown
## Prerequisites
Before starting, run `scripts/check_env.sh` to verify:
- Required tools are installed
- Target directory exists and is writable
- Dependencies are available
```

**Mode D: Script as State Detector (OpenSpec pattern)**
```bash
#!/bin/bash
# scripts/detect-state.sh <change-dir> <schema-file>
# Outputs: completed:[] ready:[] blocked:[]
```

## 6 Design Principles (Cross-Pattern)

### 1. Blueprint-First, Model Second
LLM never decides workflow path. Script/SKILL.md defines the path; LLM executes bounded sub-tasks within that path. (Source Code Agent, arXiv:2508.02721)

### 2. Dependency-Driven Progression
State transitions unlock when dependencies are met, not by external command. Prevents step-skipping and guarantees consistency.

### 3. State as Source of Truth
All behavior derives from reading current state, not inferring from history. Enables idempotency and recovery.

### 4. Instruction Injection
Provide structured context to LLM (templates, rules, dependency info) rather than letting it improvise. Reduces hallucination.

### 5. Validation Guards
Validate at every state transition. Reject invalid transitions early. Three severity levels: CRITICAL (must fix), WARNING (should fix), SUGGESTION (nice to have).

### 6. Persistent Checkpoints
Save state at key points. Long-running agents without persistence have **90% higher failure risk** (Indium Tech 2026). File system is the simplest checkpoint store.

## Quick Decision Guide

```
How many steps does your skill have?
  1-2 steps  -> Pattern 1 (file existence) or no state needed
  3-5 steps  -> Pattern 2 (checkbox tracking)
  5+ steps   -> Pattern 3 (YAML state) or Pattern 4 (schema DAG)

Does output from one invocation feed into the next?
  YES -> Need checkpointing (file existence or YAML state)
  NO  -> Stateless is fine

Are there conditional branches in the workflow?
  YES -> Pattern 3 or 4 (explicit state machine)
  NO  -> Pattern 1 or 2 (linear progression)

Do you need parallel-ready phases?
  YES -> Pattern 4 (DAG with topological sort)
  NO  -> Any simpler pattern
```

## Key Evidence

| Finding | Data | Source |
|---|---|---|
| Blueprint-First beats free-form | +10.1 pp Pass@1 | arXiv:2508.02721 |
| Compiled AI reduces tokens | 57x at scale (1000 txns) | arXiv:2604.05150 |
| Compiled AI task completion | 96% with zero runtime tokens | arXiv:2604.05150 |
| Large model output consistency | Only 12.5% (GPT-OSS-120B) | arXiv:2511.07585 |
| Small model at T=0.0 | 100% consistency | arXiv:2511.07585 |
| Long agent failure without persistence | 90% higher risk | Indium Tech 2026 |
| Generate-Validate-Fix optimal iterations | 3-5 rounds | MindStudio |
| Code-as-Action reduces steps | 30% vs ReAct | smolagents (HF) |
| OpenSpec core code | ~500 lines | OpenSpec source |
| smolagents core code | ~1,000 lines | smolagents source |
| Multi-agent token overhead | 15x vs standard dialog | Indium Tech 2026 |
| Context >20k tokens accuracy drop | 30-50% | Indium Tech 2026 |

## Sources

| Source | URL | Key Contribution |
|---|---|---|
| Source Code Agent | https://arxiv.org/abs/2508.02721 | Blueprint-First paradigm |
| Compiled AI | https://arxiv.org/abs/2604.05150 | Compile LLM output to deterministic code |
| LLM Output Drift | https://arxiv.org/abs/2511.07585 | Output consistency measurements |
| Know When To Stop | https://aclanthology.org/2024.naacl-long.202/ | Semantic drift in generation |
| Adding Determinism (IWSDS) | https://aclanthology.org/2026.iwsds-1.26.pdf | FSM vs pure prompt comparison |
| OpenSpec | Local source: `@fission-ai/openspec` | DAG artifact graph, file-as-state |
| LangGraph | https://github.com/langchain-ai/langgraph | StateGraph, checkpoint, conditional edges |
| MetaGPT | https://github.com/FoundationAgents/MetaGPT | Code=SOP(Team), ICLR 2025 oral |
| smolagents | https://github.com/huggingface/smolagents | Code-as-Action, 30% step reduction |
| MindStudio | https://www.mindstudio.ai/blog/structured-ai-coding-workflow-deterministic-agentic-nodes/ | Generate-Validate-Fix loop |
| Indium Tech | https://www.indium.tech/blog/7-state-persistence-strategies-ai-agents-2026/ | 7 persistence strategies |
| DOMINO | https://proceedings.mlr.press/v235/beurer-kellner24a.html | Constrained decoding, ICML 2024 |
| Agent-States | https://github.com/AlgorithmicResearchGroup/Agent-States | FSM for agent state |
| AgentScript | https://github.com/AgentScript-AI/agentscript | Code-as-plan, AST execution |
