---
name: results-summary-report-generator
description: Evaluate and revise an academic Results section using six evidence-based dimensions, then produce a prioritized results-quality summary report with scores, concrete problems, evidence, and actionable revisions while preserving the Results/Discussion boundary.
version: 1.0.0
---

# Results Summary Report Generator

Use this skill when the user asks to evaluate, diagnose, improve, or summarize the quality of an academic **Results** section, especially quantitative research reporting.

## Goal

Produce a structured diagnostic report that helps the user strengthen a Results section without drifting into Discussion-style interpretation. Base every judgment on the text and data the user actually provides. Do not invent statistics, methods, findings, citations, or study details.

## Inputs

Accept one or more of the following:

- a Results section or draft;
- statistical output, tables, or figure captions;
- reviewer comments about results reporting;
- a request to diagnose or revise a Results section.

If essential material is missing, state the limitation and assess only what is available. Do not fill gaps with assumed results.

## Six diagnostic dimensions

Score each dimension from **1 to 5**.

### 1. Results organization
Check whether findings are ordered logically and whether text, tables, figures, statistics, and brief factual interpretation are clearly separated and easy to follow.

### 2. Statistical reporting completeness
Check whether the reported statistics are sufficiently complete for the analysis described. When applicable, look for sample sizes, estimates, uncertainty intervals, test statistics, degrees of freedom, exact p values, effect sizes, model information, and other quantities needed to understand the result.

Do not require a statistic that is inappropriate for the method used.

### 3. Narrative-statistical alignment
Check whether numerical results, tables/figures, and prose tell the same story. Flag contradictions, unsupported adjectives, mismatched directions, omitted key results, and claims that cannot be traced to the reported evidence.

### 4. Evidence and claim calibration
Check whether the strength and scope of each claim match the evidence. Distinguish observed results from causal, mechanistic, generalizable, or explanatory claims that would require additional support.

### 5. Transparency and reproducibility of reporting
Check whether the Results section reports enough information for readers to understand what was analyzed and what was found, while avoiding Methods material that does not belong in Results. Flag selective or ambiguous reporting when it is visible from the supplied text.

### 6. Academic expression and Results-boundary control
Check clarity, precision, concision, terminology consistency, and sentence-level readability. Keep the section focused on findings. Move broad explanations, literature comparison, implications, speculation, and mechanistic interpretation to the Discussion unless the user's field or target journal explicitly requires otherwise.

## Scoring rubric

Use the following anchors consistently:

- **5 — Excellent:** complete, precise, internally consistent reporting with only negligible issues.
- **4 — Strong:** reliable reporting with minor weaknesses that do not impede interpretation.
- **3 — Adequate:** understandable but contains meaningful omissions, inconsistencies, or prioritization problems.
- **2 — Weak:** multiple important reporting problems substantially reduce clarity or evidential transparency.
- **1 — Poor:** the section cannot support a useful or reliable reading of the reported results.

Calculate the **overall score** as the arithmetic mean of the six dimension scores, rounded to one decimal place. Do not imply psychometric precision; the score is a structured editorial diagnostic.

## Workflow

1. Identify the study's reported outcomes, comparisons, models, and central result claims from the supplied material.
2. Separate factual results from interpretation, explanation, and discussion.
3. Evaluate all six dimensions independently.
4. For each identified problem, quote or point to the relevant user-provided wording or statistic when possible.
5. Classify each problem by priority:
   - **Critical:** risks changing or overstating the scientific conclusion.
   - **Major:** materially reduces clarity, completeness, or reproducibility.
   - **Minor:** wording, ordering, formatting, or local precision issue.
6. Recommend a concrete revision for every Critical or Major issue.
7. If the user asks for rewritten text, preserve the original findings and numbers exactly unless the user explicitly asks to correct a demonstrated error.
8. Re-check that the proposed revision remains inside the Results boundary.

## Output format

Use this structure unless the user requests another format:

### Overall assessment
- Overall score: X.X/5
- One-paragraph summary of the Results section's main strengths and weaknesses.

### Dimension scores
| Dimension | Score | Main reason |
|---|---:|---|
| Results organization | X/5 | ... |
| Statistical reporting completeness | X/5 | ... |
| Narrative-statistical alignment | X/5 | ... |
| Evidence and claim calibration | X/5 | ... |
| Transparency and reproducibility | X/5 | ... |
| Academic expression and boundary control | X/5 | ... |

### Priority problems
For each issue provide:
- Priority: Critical / Major / Minor
- Evidence from the supplied Results text
- Why it is a problem
- Exact revision action

### Recommended revision order
Give a short ordered sequence beginning with the changes most likely to affect scientific accuracy and interpretability.

### Optional revised Results text
Provide this section only when the user asks for rewriting or when a rewrite is clearly part of the requested deliverable. Do not create missing numerical results.

## Evidence use

Use the supporting files in `references/` as guidance for reporting principles, not as a substitute for the user's study evidence. The reference set emphasizes transparent reporting, evidence-claim alignment, statistical completeness, reproducibility, and clear scientific expression.

Useful support files:

- `references/checklist.md`
- `references/rubric.md`
- `references/references.md`
- `references/examples/example_01.md` through `example_08.md`

## Guardrails

- Never fabricate or infer unreported numerical values.
- Never convert association into causation without an appropriate design and evidence.
- Never declare significance from direction or magnitude alone.
- Never treat a non-significant result as proof of no effect.
- Never move literature review, broad implications, mechanisms, or speculation into Results merely to make the prose sound stronger.
- Preserve the user's terminology and statistical notation unless correcting a clear inconsistency.
- If the supplied evidence is insufficient for a confident judgment, say so explicitly.
