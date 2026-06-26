# Self-Discover Reasoning Skill

> An AI agent skill for self-composing task-specific reasoning structures.
> Based on Zhou et al. (2024) — SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures.

## Platform Auto-Detection

At skill load time, detect your runtime environment and adjust capabilities:

| Capability | How to Check | Fallback
|-----------|-------------|----------|
| File system | Can you read `references/discovery-templates.md`? | Use the inline templates below instead
| Persistent memory | Can you write to `memory/`? | Store discovery notes in conversation context only
| Long context | Is your context window > 32K tokens? | Cap at Level 2 (skip full discovery)
| Tool access | Can you call external tools? | Use mental reasoning only |

**Detection rules:**
- If you can read this file's `references/` directory → full mode (all levels + memory)
- If you can read files but not write → full levels, in-conversation memory only
- If you cannot read files at all → use inline templates (copied below), cap at Level 2
- If context is limited (< 8K usable) → default to Level 1, max Level 2

This means **every platform gets the best possible experience automatically** — no manual configuration needed.

## Inline Discovery Templates (for environments without file access)

If you cannot read `references/discovery-templates.md`, use these directly:

### Level 1 Internal Prompt
```
Before answering: (1) What type of reasoning does this task need? (2) Pick 1-2 modules from the seed list. (3) Apply them. Deliver.
```

### Level 2 Internal Prompt
```
1. SELECT: From the seed modules, choose 3-5 relevant to this task.
2. ADAPT: Rephrase each selected module to be task-specific.
3. IMPLEMENT: Compose into a step-by-step reasoning structure.
4. Follow the structure to produce the answer.
```

### Level 3 Internal Prompt
```
1. SELECT: Choose 4-7 modules relevant to the task type.
2. ADAPT: Tailor each to the specific task, adding domain expertise.
3. IMPLEMENT: Build a JSON-like reasoning structure with keys and expected outputs.
4. Execute the structure step-by-step.
5. VERIFY: Check the answer against the structure — did every key get a valid value?
6. If gaps found, refine the structure and re-execute.
```

## When to Activate

Activate when you are about to solve a **reasoning-intensive task** — after gathering all information but before producing your answer. Discovery happens *before* reasoning, not instead of work.

**Strong triggers:** Multi-step reasoning, math, logic puzzles, planning, debugging, architecture decisions, analytical tasks.

**Skip:** Simple factual lookups, greetings, formatting requests, single-sentence answers.

## Core Process: SELECT → ADAPT → IMPLEMENT → SOLVE

```
1. SELECT    — Choose relevant reasoning modules from the seed set
2. ADAPT     — Rephrase selected modules to be task-specific
3. IMPLEMENT — Compose modules into a structured reasoning plan (key-value format)
4. SOLVE     — Follow the reasoning structure to produce the final answer
```

Source: Zhou et al., "Self-Discover: Large Language Models Self-Compose Reasoning Structures" (2024, ICML) — LLMs self-compose atomic reasoning modules into task-intrinsic structures, achieving up to 32% improvement over Chain-of-Thought.

---

## Seed Reasoning Modules

These are atomic reasoning skills drawn from cognitive science and prompting research (Fernando et al., 2023; Zhou et al., 2024). The agent selects a subset relevant to each task.

| # | Module | Description | Best For |
|---|--------|-------------|----------|
| 1 | **Step-by-Step Thinking** | Break reasoning into sequential steps | Sequential tasks, procedures |
| 2 | **Decomposition** | Break problem into sub-problems, solve each | Complex multi-part problems |
| 3 | **Critical Thinking** | Analyze from multiple perspectives, question assumptions | Evaluating claims, decisions |
| 4 | **Reflective Thinking** | Search for first principles, examine underlying theory | Science, deep analysis |
| 5 | **Creative Thinking** | Generate novel approaches, brainstorm alternatives | Design, open-ended tasks |
| 6 | **Pattern Recognition** | Identify recurring patterns and regularities | Data analysis, sequences |
| 7 | **Analogical Reasoning** | Map solutions from similar known problems | Transfer learning, explanations |
| 8 | **Causal Analysis** | Identify cause-effect relationships | Debugging, diagnostics |
| 9 | **Constraint Satisfaction** | Check solutions against all constraints | Optimization, planning |
| 10 | **Abstraction** | Extract general principles from specifics | Generalization, architecture |
| 11 | **Hypothesis Testing** | Form and test hypotheses systematically | Troubleshooting, debugging |
| 12 | **Comparative Analysis** | Compare options against defined criteria | Decision-making, trade-offs |
| 13 | **Temporal Reasoning** | Reason about sequences and time dependencies | Scheduling, process flows |
| 14 | **Spatial Reasoning** | Reason about spatial relationships | Layout, geometry, UI |
| 15 | **Counterfactual Thinking** | Consider "what if" alternatives | Risk analysis, planning |
| 16 | **Lateral Thinking** | Approach from unconventional angles | Innovation, problem-solving |
| 17 | **Deductive Reasoning** | Apply general rules to specific cases | Logic, validation |
| 18 | **Inductive Reasoning** | Infer general rules from specific examples | Pattern generalization |
| 19 | **Probabilistic Thinking** | Reason under uncertainty with probabilities | Risk assessment, forecasting |
| 20 | **Systems Thinking** | Consider interactions between components | Architecture, complex systems |

---

## Discovery Depth Levels

The depth is determined by **task complexity**, not user preference. The agent auto-selects.

### Level 0: Direct Answer (Skip discovery)

**Trigger:** Simple factual lookups, greetings, trivial questions, single-sentence answers.

**Action:** Do nothing extra. Just respond. Cost: 0 additional tokens.

**Examples:** "What time is it?", "Thanks", simple formatting requests.

### Level 1: Single-Module Reasoning

**Trigger:** Medium-complexity tasks — explanations, how-to guides, code snippets, questions requiring one type of reasoning.

**Action:** Select 1-2 relevant modules. Apply mentally. Deliver.

**Budget:** 1 discovery pass. ~10% overhead on response tokens.

**Internal process:**
```
After receiving the task:
- What type of reasoning does this need?
- Pick the most relevant module (e.g., "decomposition" for multi-part questions)
- Apply it while composing the answer
- Deliver
```

### Level 2: Multi-Module Composition

**Trigger:** Complex tasks — technical architectures, multi-step plans, debugging, anything requiring 3+ reasoning steps or multiple perspectives.

**Action:** Select 3-5 modules. Adapt to task. Compose into structured plan. Execute.

**Budget:** 1 full discovery cycle (SELECT + ADAPT + IMPLEMENT). ~25% overhead.

**Internal process:**
```
1. SELECT 3-5 relevant modules from the seed set
2. ADAPT each to be specific to this task
3. IMPLEMENT into a step-by-step structure
4. Follow the structure to produce the answer
```

### Level 3: Full Self-Discovery

**Trigger:** High-stakes tasks — complex math, logic puzzles, production architecture, multi-constraint optimization, or user explicitly requests thorough reasoning.

**Action:** Full SELECT → ADAPT → IMPLEMENT cycle with 4-7 modules, JSON-like reasoning structure, and verification pass.

**Budget:** Full discovery cycle + verification. ~40% overhead.

**Internal process:**
```
1. SELECT 4-7 relevant modules
2. ADAPT with domain-specific tailoring
3. IMPLEMENT into key-value reasoning structure:
   {
     "step_1": { "action": "...", "expected_output": "..." },
     "step_2": { "action": "...", "expected_output": "..." },
     ...
   }
4. Execute each step, filling in values
5. VERIFY: Did every step produce a valid output?
6. If gaps → refine structure, re-execute gap steps only
```

---

## Pre-Built Discovery Structures (Quick Templates)

For common task types, use these pre-composed structures instead of running full discovery:

### Coding / Debugging
```json
{
  "step_1": { "action": "Reproduce: Identify the exact error and trigger condition", "output": "error description" },
  "step_2": { "action": "Decompose: Break the code path into segments", "output": "list of code segments" },
  "step_3": { "action": "Hypothesis: Form 2-3 hypotheses for root cause", "output": "ranked hypotheses" },
  "step_4": { "action": "Test: Verify top hypothesis against evidence", "output": "confirmed root cause" },
  "step_5": { "action": "Fix: Implement the fix with edge case handling", "output": "corrected code" }
}
```

### Architecture / Decision
```json
{
  "step_1": { "action": "Decompose: List all requirements and constraints", "output": "requirement matrix" },
  "step_2": { "action": "Compare: Generate 2-3 options", "output": "option summaries" },
  "step_3": { "action": "Evaluate: Score each option against constraints", "output": "comparison table" },
  "step_4": { "action": "Decide: Select best option with justification", "output": "decision + rationale" },
  "step_5": { "action": "Validate: Check for overlooked constraints", "output": "final recommendation" }
}
```

### Math / Logic
```json
{
  "step_1": { "action": "Understand: Restate the problem, identify given and unknown", "output": "problem statement" },
  "step_2": { "action": "Plan: Select relevant formulas/approaches", "output": "solution strategy" },
  "step_3": { "action": "Execute: Apply step-by-step with intermediate results", "output": "workings" },
  "step_4": { "action": "Verify: Substitute answer back or check invariants", "output": "verification" }
}
```

### Analysis / Research
```json
{
  "step_1": { "action": "Scope: Define what needs to be analyzed and why", "output": "analysis scope" },
  "step_2": { "action": "Gather: Identify key facts, data points, or evidence", "output": "evidence list" },
  "step_3": { "action": "Pattern: Find patterns, trends, or anomalies", "output": "findings" },
  "step_4": { "action": "Synthesize: Combine findings into conclusions", "output": "conclusions" },
  "step_5": { "action": "Validate: Check conclusions against original scope", "output": "final analysis" }
}
```

---

## Convergence Rules

Based on the empirical finding from Zhou et al. that self-discovered structures are effective in a single pass:

1. **Maximum 1 discovery cycle** per task (SELECT → ADAPT → IMPLEMENT is one cycle).
2. **Verification pass** (Level 3 only): If verification reveals gaps, refine structure once. Do not loop.
3. **Stop if** the structure covers all aspects of the task.
4. **Diminishing returns rule**: Discovery overhead should never exceed 40% of the response.

**Anti-pattern — DO NOT:**
- Run discovery on every single message (use Level 0 for simple Q&A)
- Over-compose modules (more ≠ better; 3-5 modules is optimal for most tasks)
- Re-run discovery if the first answer is reasonable

---

## Cost Control Strategy

| Depth | Modules | Max Steps | Approx. Token Overhead | When to Use |
|-------|:-------:|:---------:|:----------------------:|-------------|
| Level 0 | 0 | 0 | +0% | Simple Q&A |
| Level 1 | 1-2 | Mental | ~10% | Most conversations |
| Level 2 | 3-5 | Structured plan | ~25% | Complex technical |
| Level 3 | 4-7 | Full JSON + verify | ~40% | High-stakes only |

**Principle:** Discovery should cost less than the cost of a wrong approach. For low-stakes responses, skip discovery entirely.

---

## Trigger Conditions Summary

### Auto-Trigger (always on)
- Task requires multi-step reasoning → at least Level 1
- Task involves 3+ distinct reasoning types → at least Level 2
- Task is math, logic, or planning → at least Level 1

### Skip Discovery
- User is in a hurry (explicit: "quick", "brief", "just tell me")
- Response is under 2 sentences
- Pure social/chat exchange
- Simple factual lookup

### User Manual Trigger
- User says "think carefully", "reason through this" → Level 2+
- User says "this is important", "critical", "production" → Level 3
- User says "discover" or "self-discover" → Level 2+

---

## Output Format

Discovery is **internal** — the user should not see the raw reasoning structure. However:

### After using discovery, you MAY append a subtle note:

**Level 1:** No note (keep it invisible).
**Level 2:** Optionally: `_(response composed via multi-module reasoning)_`
**Level 3:** Optionally: `_(reasoning structure self-discovered from [N] modules)_`

### NEVER:
- Show the raw JSON reasoning structure to the user
- Make the note prominent or distracting
- Add notes for Level 0 or Level 1 responses

---

## Cross-Task Transfer (Structure Reuse)

Inspired by Zhou et al.'s finding that self-discovered structures transfer across model families — the same reasoning structure that works for GPT-4 also helps Llama-2.

**When to reuse:** When you encounter a task of the same type as one you've previously solved with discovery (e.g., another debugging task, another architecture decision).

**How to reuse:** Write the discovered structure to `memory/discovered-structures.md`:
```
## [Task Type]
Structure: [paste the key-value structure]
Effective for: [describe task characteristics]
Date: [today]
```

Next time you encounter a similar task, check memory first before running discovery again.

---

## Relationship to Other Reasoning Techniques

| Technique | Source | How Self-Discover Differs |
|-----------|--------|---------------------------|
| **Chain of Thought** | Wei et al. 2022 | CoT is a single module; Self-Discover composes multiple |
| **Least-to-Most** | Zhou et al. 2022 | Decomposition only; Self-Discover selects best modules per task |
| **Self-Consistency** | Wang et al. 2022 | Requires 10-40x more compute; Self-Discover is more efficient |
| **Tree of Thoughts** | Yao et al. 2023 | Explores multiple paths; Self-Discover composes optimal structure |
| **Step-Back Prompting** | Zheng et al. 2023 | Single principle; Self-Discover combines multiple heuristics |
| **OPRO** | Yang et al. 2023 | Optimizes prompts with training data; Self-Discover needs no labels |

---

## Quick Reference Card

```
DISCOVER? ──→ Simple/trivial? ──→ NO → Just respond
    │
    YES
    │
    ├─ Single reasoning type → LEVEL 1 (1-2 modules, mental)
    ├─ Multi-step / multi-perspective → LEVEL 2 (3-5 modules, structured)
    └─ High-stakes / complex → LEVEL 3 (4-7 modules, full JSON + verify)

SELECT → ADAPT → IMPLEMENT → SOLVE
    │          │          │          │
    Pick      Tailor     Structure  Execute
    modules   to task    the plan   the plan
```
