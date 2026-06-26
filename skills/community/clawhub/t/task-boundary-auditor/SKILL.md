---
name: task-boundary-auditor
description: Use when a user asks the AI to perform tasks that may exceed LLM capabilities, such as counterfactual reasoning, formal verification, real-time control, physical design, ethical judgment, zero-omission auditing, or extreme prediction. Also use when tasks mix safe and unsafe sub-tasks. Triggers: "verify all", "prove", "predict", "design a bridge/system", "what if X never happened", "ensure no omissions", "real-time monitor", "legal/medical judgment".
---

# Task Boundary Auditor

## Overview

When an LLM oversteps its boundaries, it does not say "I can't do this." Instead, it delivers answers that are perfectly formatted and logically coherent—but fundamentally wrong. This is the **sophisticated hallucination**. This Skill performs a rapid pre-execution audit to determine whether a task exceeds LLM capabilities, and proposes a human-machine division of labor: what the LLM can handle, and what must be handed off to specialized tools or humans.

## When to Use

- The user asks the LLM to perform causal inference, precise verification, real-time control, physical design, or other tasks beyond its capabilities
- The user demands completeness guarantees such as "zero omissions," "find all," or "ensure none are missed"
- The user requests counterfactual reasoning ("what if X had never happened")
- The task mixes safe and unsafe sub-tasks

## When NOT to Use

- Pure text generation, translation, summarization, or format conversion (safe-zone tasks—execute directly)
- The user already clearly understands that human/professional tools are needed
- Simple information retrieval or Q&A

## Boundary Classification

### Prohibited Zone (LLM must not take primary responsibility)

| Type | Detection Signature | Core Characteristic | Correct Approach |
|------|---------------------|---------------------|------------------|
| **Counterfactual Reasoning** | Hypothetical worlds, long causal chains | LLM has no world model; can only assemble narratives | Causal models / expert reasoning; LLM extracts evidence |
| **Precise Verification** | Symbolic proof, code audit, zero omissions | Error in long-chain reasoning compounds exponentially | Formal tools / expert verification; LLM translates specifications |
| **Real-Time Closed-Loop** | Cross-call state retention, sense-act-feedback | LLM is stateless and has no sensor interfaces | Rule engines / control systems; LLM writes logs |
| **Physical Intuition** | Spatial-mechanical-material reasoning | LLM's understanding of physics is second-hand text | CAD / simulation software; LLM interprets results |
| **Conceptual Extrapolation** | Creative breakthroughs, out-of-training-distribution | Can only interpolate and recombine; cannot extrapolate | Human provides core insight; LLM assists with association |
| **Ethical Adjudication** | Requires subjectivity and legal liability | LLM has no subjectivity or capacity for responsibility | Human adjudication; LLM structures the framework |
| **Zero-Omission Audit** | Completeness guarantee, blind-spot-free scan | Generative review has attention blind spots | Rule-engine scan; LLM assists with explanation |
| **Extreme Prediction** | Out-of-distribution events, black swans | Forcibly translates into known patterns | Causal rule-layer reasoning; LLM performs extraction |

### Safe Zone (LLM can take primary responsibility)

| Type | Examples |
|------|----------|
| **Text Generation** | Writing emails, drafting articles |
| **Translation & Conversion** | Chinese-English translation, format conversion |
| **Information Extraction** | Extracting data or key points from reports |
| **Summarization & Compression** | Paper summaries, meeting minutes |
| **Formatting** | Converting to tables, generating templates |

### Restricted Zone (LLM assists; human / professional tools take primary responsibility)

| Type | Characteristic | Constraint |
|------|----------------|------------|
| **Short-Chain Causality** | 2–3 step causality based on explicit associations | LLM extracts evidence; human / model makes judgment |
| **Numerical Estimation** | Order-of-magnitude or range; no precise verification needed | Must be labeled "estimate, not precise" |
| **Draft Proposal** | Drafts requiring human confirmation | LLM generates options; human selects and takes responsibility |
| **Known Pattern Matching** | Within training distribution but requires professional judgment | LLM organizes information; professional system diagnoses |

## Audit Workflow

```
1. Parse task → extract [verb] + [object] + [constraints]
2. Match boundary → classify against the table above: Prohibited / Restricted / Safe
3. Output verdict → provide division-of-labor plan based on classification
```

Mixed tasks (involving both safe-zone and prohibited-zone elements) must be decomposed into sub-tasks and classified individually.

## Output Templates

Select the appropriate output based on the classification:

### Boundary Violation Block

```
## Task Boundary Audit

Task: [one-sentence description]
Verdict: ❌ [Violation Type] — [Reason]

Sophisticated Hallucination Risk: [specific description of how the LLM will pretend it can do this]

Recommended Division of Labor:
- LLM: [what the LLM can do, e.g., extract evidence, translate, format]
- Professional tools / human: [what must be handed off, e.g., causal reasoning, verification, adjudication]
- Next step: [concrete action the user can take]
```

### Restricted Task Routing

```
## Task Boundary Audit

Task: [one-sentence description]
Verdict: 🟡 [Restricted Type]

Task Decomposition:
| Sub-task | Responsible Party | Constraint |
|----------|-------------------|------------|
| [...] | LLM | [...] |
| [...] | Human / tool | [...] |

Risk Point: [the step where the LLM is most likely to pretend it is competent]
Mandatory Disclaimer: LLM output must include "This conclusion is based on text extraction, not verification."
```

### Safe Clearance

```
## Task Boundary Audit

Task: [one-sentence description]
Verdict: ✅ Safe

Execution Recommendation:
- LLM executes directly
- Cross-check factual claims when involved
- Recommend human spot-check of 10%–20%
```

## Usage Examples

### Violation: Zero-Omission Audit

> User: Review this 200-page investment agreement, find all hidden clauses, and guarantee no omissions.
>
> Agent: Task Boundary Audit → ❌ Zero-Omission Audit. LLM review is generative and has attention blind spots (may miss footnotes, appendices, cross-references); it cannot provide a completeness guarantee.
>
> **Sophisticated Hallucination Risk**: The AI will return a perfectly formatted report with precise clause locations and professional risk descriptions. Yet the put option buried in Appendix C may be "elegantly" overlooked.
>
> **Division of Labor**: LLM structures the agreement by section and extracts explicit risk clauses → rule engine scans for known risk patterns → lawyer reviews clause by clause and assumes responsibility.

### Restricted: Causal Analysis + Prediction

> User: Analyze this sales data, identify the causes of the decline, and predict next quarter's trend.
>
> Agent: Task Boundary Audit → 🟡 Short-Chain Causality (LLM can extract known decline factors) + ❌ Trend Prediction (out-of-distribution prediction, prohibited).
>
> **Decomposition**:
> | Sub-task | Responsible Party | Constraint |
> |----------|-------------------|------------|
> | Extract decline factors mentioned in the report | LLM | Verify completeness |
> | Determine primary causes and factor interactions | Human / statistical model | LLM must not output causal conclusions |
> | Predict next quarter's sales | Statistical model / expert | LLM must not output precise predictions |
> | Describe historical trends (not predictions) | LLM | Label as "historical description, not future prediction" |

### Safe: Translation + Extraction

> User: Translate this English contract into Chinese and extract the payment clauses.
>
> Agent: Task Boundary Audit → ✅ Translation & Conversion + ✅ Information Extraction. LLM executes directly. Recommend human spot-check of payment clause amounts, dates, and conditions.

## Common Mistakes

- **Downgrading the verdict because the user insists**: User urgency or insistence does not reduce risk; classification criteria remain unchanged.
- **Equating "LLM is good at search" with "LLM can verify"**: LLM can extract information, but that does not equal judging correctness.
- **Auditing only part of a mixed task**: If a task contains one prohibited sub-task, the entire task must be decomposed.
- **Underestimating the subtlety of sophisticated hallucinations**: The most dangerous outputs are not obvious nonsense, but professionally polished answers that are fundamentally wrong.
- **Treating restricted zones as safe zones**: Numerical estimates must be labeled with uncertainty; draft proposals must be labeled as pending confirmation.

## Notes

- The classification rules in this Skill are human-hardened; the Agent must not modify the boundary classification table.
- The Agent enforces classifications strictly and must not downgrade risk due to vague phrasing or user pressure.
- Judgments involving legal, medical, financial, or other professional domains should recommend human review even when technically feasible.
