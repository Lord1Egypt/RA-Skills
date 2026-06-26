---
name: structure-thinking
description: Structured problem analysis and communication using system mapping and hierarchical logic. Use when a request involves messy, multi-factor problems, root-cause analysis, intervention design, feedback loops or delays, or when a clear top-line recommendation with logically grouped support is required.
---

# Structure Thinking

## Overview
Use this skill to turn a messy situation into a clear decision path. You will model the system to find real levers, then build a compact argument that enables action. The focus is practical: define the decision, diagnose the system behavior, choose interventions, and communicate a decisive recommendation.

## Preferred Inputs
- Decision owner and deadline.
- Success definition (metric, threshold, or observable change).
- Constraints (budget, time, policy, technical limits).
- Behavior over time (trend, seasonality, oscillation).

If any are missing and the user wants an answer now, proceed with explicit assumptions and mark them as `Assumed`.

## Workflow

### 1) Define the Decision and Question
Goal: one clear governing question and a provisional answer.

Do:
- Write a one-sentence decision statement: “Decide whether to X by date Y to achieve Z.”
- Capture `Situation`, `Complication`, `Question`, `Answer`.
- List assumptions and unknowns explicitly.

Output:
- Governing question.
- Provisional answer in one sentence.

### 2) Describe Behavior Over Time
Goal: pin the problem to a trend, not a feeling.

Do:
- Summarize how the key metric changes over time.
- Note seasonality, spikes, or oscillations.
- State the time horizon that matters.

Output:
- Behavior-over-time summary (2-4 bullets).

### 3) Model the System
Goal: explain why the behavior persists.

Do:
- Define system boundary and stakeholders.
- Identify 1-3 critical stocks and their flows.
- Draw reinforcing and balancing loops.
- Mark delays and missing information.

Output:
- System map notes: stocks, flows, loops, delays.

### 4) Generate Hypotheses (MECE)
Goal: create testable explanations or options.

Do:
- Build an issue tree with 3-5 MECE branches.
- Label each branch as an assertion (not a topic).
- Rank branches by impact and evidence availability.

Output:
- Issue tree with ranked branches.

### 5) Select Leverage Points and Interventions
Goal: choose a small set of actions that change structure, not just parameters.

Do:
- Map top branches to leverage points.
- Propose 1-3 interventions and how they change the system.
- Identify risks, side effects, and where resistance will appear.

Output:
- Intervention shortlist with mechanism + risks.

### 6) Build the Argument Hierarchy
Goal: make the decision obvious and actionable.

Do:
- Lead with the answer.
- Add 2-5 support points, each an assertion.
- Place evidence under each support.
- Keep each layer MECE and parallel.

Output:
- Decision-ready outline (top-line + supports + evidence).

### 7) Validate and Iterate
Goal: avoid false confidence.

Do:
- Run counterfactuals and ask what would disprove the answer.
- Check for feedback delays and unintended consequences.
- Update the system model and argument as evidence changes.

Output:
- Final recommendation with confidence level and known gaps.

## When Inputs Are Missing
Deliver a best-effort output with explicit assumptions.

Use this format:
- `Assumed`: list what you assumed and why.
- `Open questions`: list what would change the answer most.
- `Provisional diagnosis`: short system explanation.
- `Interventions`: 2-3 actions with risks.

Do not block the answer unless the user explicitly asks you to wait.

## Practical Prompts
Use these to move fast when information is incomplete.

Decision framing:
- “What single decision are we making, by when, and who owns it?”
- “What does success look like in one metric?”

Behavior over time:
- “Show the metric trend for the last N weeks/months.”
- “Where are the spikes, delays, or oscillations?”

System modeling:
- “What is the main stock that is accumulating or draining?”
- “Which loop is reinforcing the problem?”
- “Where is the delay that hides the effect?”

Interventions:
- “Which rule change would prevent the loop from amplifying?”
- “Which information flow, if made visible, would change behavior?”

## Intervention Checklist
For each proposed action, answer:
- Mechanism: which loop or stock does it change?
- Owner: who can implement it?
- Trigger: when does it take effect?
- Metric: what leading indicator confirms it works?
- Risk: what side effect or resistance might appear?

## Evidence Quick Check
- Baseline: what is the current level and trend?
- Attribution: what evidence links cause to effect?
- Counterfactual: what would disprove this claim?
- Lag: how long until impact should show up?

## Output Templates

Decision memo (short):
- Answer (1 sentence)
- Why now (1-2 sentences)
- Key supports (2-5 bullets)
- Evidence per support (2-4 bullets)
- Intervention plan (actions, owner, timing)
- Risks and mitigations

System summary (short):
- Boundary and actors
- Key stocks and flows
- Dominant loops
- Delays and information gaps

## Mini Example (Software)
Problem: API latency spikes during peak traffic.

Decision statement:
- Decide whether to change retry and rate-limit policy this quarter to stabilize p95 latency.

Provisional answer:
- Yes, reduce retry amplification and shorten scaling delay.

Top-line outline:
- Answer: change retry and rate-limit rules and adjust scaling thresholds.
- Support 1: retry amplification dominates peak load.
- Support 2: scaling delay creates overshoot.
- Support 3: policy changes reduce queue growth without lowering throughput.

## Common Failure Modes
- Jumping to solutions without modeling the system.
- Mixing causes, solutions, and evidence in one layer.
- Optimizing a local metric that harms the whole system.
- Parameter tweaks that ignore feedback or delays.
- Vague supports with no mechanism or evidence.

## Reference Map
- Load `references/structured-communication-core.md` for hierarchical logic, MECE, SCQA, and writing rules.
- Load `references/systems-dynamics-core.md` for system concepts, leverage points, and practice rules.
- Load `references/integrated-framework.md` for the unified method and example.
- Load `references/software-playbooks.md` for software-focused playbooks.
