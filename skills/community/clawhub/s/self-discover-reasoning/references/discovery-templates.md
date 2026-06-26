# Discovery Prompt Templates

Internal prompt templates the agent uses during the SELECT → ADAPT → IMPLEMENT pipeline. These are NOT shown to users.

---

## Level 1: Single-Module Discovery Prompt (Internal)

```
You have a task to solve. First, identify which reasoning approach fits best:

TASK TYPE DETECTION:
- Is this a step-by-step procedure? → DECOMPOSITION
- Does this require finding patterns? → PATTERN_RECOGNITION
- Does this need causal explanation? → CAUSAL_ANALYSIS
- Is this about abstracting principles? → ABSTRACTION
- Does this need creative generation? → DIVERGENT_THINKING
- Is this about evaluating options? → CRITICAL_THINKING

Apply the selected module's template to structure your reasoning, then answer.
```

---

## Level 2: Multi-Module Composition Prompt (Internal)

```
You are composing a reasoning structure for a complex task.

## Phase 1: SELECT
Review the seed reasoning modules. Select 2-3 that are most relevant:

### Seed Modules:
1. **DECOMPOSITION** — Break into sub-problems, solve each
2. **PATTERN_RECOGNITION** — Identify recurring structures/patterns
3. **ABSTRACTION** — Extract general principles from specifics
4. **CAUSAL_ANALYSIS** — Trace cause → effect chains
5. **CRITICAL_THINKING** — Evaluate claims, find assumptions
6. **CONSTRAINT_SATISFACTION** — Identify and satisfy constraints
7. **ANALOGICAL_REASONING** — Map from known to unknown
8. **DIVERGENT_THINKING** — Generate multiple alternatives

For this task, the most relevant modules are: [select and justify]

## Phase 2: ADAPT
Combine the selected modules into a unified reasoning structure:
- How do the modules connect?
- What is the order of operations?
- What should each module produce as intermediate output?

Write the adapted structure as a numbered plan.

## Phase 3: IMPLEMENT
Follow your adapted structure step by step. At each step, verify the output
makes sense before proceeding. If a step fails, reconsider the structure.

## Phase 4: EVALUATE
After completing, check:
- Did I answer the original question fully?
- Is the reasoning sound?
- Could a simpler structure have worked?
```

---

## Level 3: Full SELF-DISCOVER Prompt (Internal)

```
You are constructing a custom reasoning structure from first principles.
This is a high-complexity task requiring careful thought.

## Phase 1: TASK ANALYSIS
Analyze the task deeply:
- What type of problem is this? (classification, generation, optimization, analysis, planning)
- What are the key constraints?
- What makes this problem hard?
- What kind of output is expected?
- What are common failure modes for this type of task?

## Phase 2: SELECT
From the full set of seed reasoning modules, select the most relevant ones.

### Full Module Catalog:

**Analytical Modules:**
1. DECOMPOSITION — Break complex problem into independent sub-problems
2. PATTERN_RECOGNITION — Identify recurring structures, trends, regularities
3. ABSTRACTION — Move from concrete to general, extract principles
4. CAUSAL_ANALYSIS — Map cause-effect relationships, identify root causes

**Evaluative Modules:**
5. CRITICAL_THINKING — Challenge assumptions, evaluate evidence quality
6. CONSTRAINT_SATISFACTION — Enumerate constraints, verify each is met
7. VERIFICATION — Cross-check claims against known facts or logic

**Generative Modules:**
8. ANALOGICAL_REASONING — Map structure from familiar domain to new domain
9. DIVERGENT_THINKING — Generate multiple distinct approaches
10. SYNTHESIS — Combine disparate elements into coherent whole

**Structural Modules:**
11. SEQUENTIAL_PLANNING — Order steps with dependencies
12. HIERARCHICAL_ORGANIZATION — Organize into levels of abstraction
13. COMPARATIVE_ANALYSIS — Systematically compare options across dimensions

For each selected module, explain WHY it helps for THIS specific task.

## Phase 3: ADAPT
Transform the selected modules into a concrete, task-specific reasoning plan:

For each module:
1. What specific question does it answer for this task?
2. What is the input → transformation → output?
3. How does its output feed into the next module?

Write the complete adapted structure as an ordered plan with clear milestones.

## Phase 4: IMPLEMENT
Execute your adapted structure:
- Follow each step precisely
- At milestones, verify intermediate results
- If a step produces unexpected results, diagnose and adapt
- Keep track of which modules contributed most value

## Phase 5: EVALUATE & REFINE
After completion:
1. Check completeness — did the structure cover everything?
2. Check efficiency — were any modules unnecessary?
3. Check correctness — is the final answer sound?
4. Note the discovered structure for future reuse

If significant issues found → refine the structure and re-execute (max 1 retry).
```

---

## Task-Type Heuristic Templates

Quick classification heuristics for auto-selecting depth level:

```
CLASSIFY THE TASK:

**Level 0 (direct answer):**
- Factual lookup ("What is X?")
- Simple formatting
- Social/chat
- Under 2 sentences expected

**Level 1 (single module):**
- Single-step explanation
- Code snippet with clear pattern
- Comparison of 2-3 items
- How-to with known steps

**Level 2 (multi-module):**
- Multi-step problem solving
- Architecture/design decisions
- Analysis requiring multiple perspectives
- Tasks with 3+ distinct sub-problems

**Level 3 (full discovery):**
- Novel or rare problem types
- Tasks requiring creative solutions
- Problems with many constraints
- Multi-domain integration
- High-stakes decisions
```

---

## Discovered Structure Cache Template

For saving successful reasoning structures for reuse across sessions.

```markdown
## Discovered Reasoning Structure
- **Date:** [YYYY-MM-DD]
- **Task Type:** [e.g., "debugging distributed systems", "API design"]
- **Task Signature:** [brief pattern that matches similar tasks]
- **Modules Used:** [list modules in order]
- **Adapted Structure:** [the concrete plan that worked]
- **Effectiveness:** [how well it worked, 1-5 stars]
- **Notes:** [what to adjust next time]
```

Write to `memory/discovered-structures.md` (append, don't overwrite).
