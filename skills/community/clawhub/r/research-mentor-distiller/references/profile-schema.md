# Research Mentor Distillation Schema

Use this schema to extract evidence before writing a mentor skill. Keep claims short, grounded, and tagged by confidence.

## Source Record

- Source id:
- Source type: homepage, CV, paper, talk, interview, project page, code, dataset card, user-provided note
- Title:
- Year:
- URL or local path:
- Direction/topic:
- Confidence: direct evidence, strong inference, speculative extension

## Per-Paper Extraction

Prefer full text when available. If only title, abstract, or project page is
available, mark the confidence lower and do not use the signal as sole support
for core methodology claims.

### Problem Framing

- What gap does the paper claim exists?
- What existing framing does it reject or refine?
- What real-world capability motivates the work?
- What would make this problem important beyond the benchmark?

### Contribution Type

Mark all that apply:

- Dataset or benchmark
- Model or architecture
- Training objective
- Data engine or annotation pipeline
- Evaluation protocol
- System or agent
- Theory or analysis
- Domain application
- Open-source artifact

### Data And Supervision

- Main data source:
- Label source:
- Scalable supervision source:
- Human expert involvement:
- Synthetic or pseudo-label component:
- Retrieval, ontology, report, or web-scale source:
- Data quality risks:

### Methodology Pattern

- Core technical move:
- Reused methodological motif:
- Simplicity vs complexity:
- Engineering/system emphasis:
- Theoretical emphasis:
- Domain knowledge usage:

### Evaluation Taste

- Main datasets:
- Main metrics:
- Baseline families:
- Ablations:
- Human/domain evaluation:
- Error analysis:
- Generalization or robustness tests:
- What result would actually convince a skeptical reviewer?

### Writing And Presentation

- Title pattern:
- Abstract structure:
- Claim style:
- Figures/tables:
- Qualitative examples:
- Failure cases:
- Limitations:

### Taste Signal

Write 1-3 bullets:

- This paper suggests the scholar values...
- This paper suggests the scholar is skeptical of...
- This paper suggests a good problem should...

### Full-Text Precision Signals

Use these only after reading the paper body, not just the abstract:

- Introduction claim: what bottleneck is elevated as the real problem?
- Method core: what technical move turns the framing into a system or experiment?
- Data engine: what data, supervision, ontology, reports, pseudo-labels, or web sources make the work possible?
- Evaluation contract: what baselines, ablations, metrics, expert checks, or robustness tests are treated as decisive?
- Failure boundary: what the authors admit is not solved, or what their setup quietly excludes?
- Artifact value: dataset, benchmark, code, model, web demo, clinical/scientific pipeline, or reusable protocol.
- Reusable mentoring rule: how this paper should change advice on a new research idea.

## Cross-Paper Synthesis

### Worldview

Only include claims supported by several sources. Ask:

- What does this scholar think the field is really trying to solve?
- What bottleneck appears repeatedly?
- What kind of intelligence, system, or theory is the long-term target?

### Problem Ontology

Classify recurring problems:

- Capability gaps
- Data bottlenecks
- Evaluation blind spots
- Domain translation gaps
- Scaling or deployment gaps
- Conceptual reframings

### Methodology Repertoire

List recurring moves:

- Data construction
- Self/weak supervision
- Multimodal fusion
- Retrieval or knowledge augmentation
- Memory/reasoning/agentic workflow
- Domain-specific evaluation
- Open-source release

### Core Methodology Across Directions

Promote a pattern into the scholar's core methodology only when it passes at
least two of these checks:

- Recurs in at least three papers.
- Recurs across at least two directions.
- Appears in method or experiment sections, not only in titles.
- Has a distinct tradeoff or exclusion, not a generic "use strong baselines" rule.

For each core methodology, record:

- Name:
- Short rule:
- Evidence papers:
- Where it appears: problem framing, data, method, evaluation, writing, release
- Why it is distinctive:
- When to apply:
- When not to apply:
- Confidence: direct evidence, strong inference, speculative extension

### Direction-Specific Methodology

Create separate methodology notes when the scholar's directions require
different playbooks. Typical dimensions:

- Direction name:
- Target capability:
- Preferred problem type:
- Data and supervision pattern:
- Method pattern:
- Evaluation pattern:
- Common failure modes:
- Representative papers:
- Confidence:

Do not force a unified worldview when the evidence shows direction-specific
rules. Keep tensions visible.

### Decision Heuristics

Each heuristic should be actionable and evidence-linked:

- If a new idea lacks X, push for Y.
- If the dataset is weak, ask Z.
- If the claim is broad, require evaluation A and baseline B.

### Anti-Patterns

List ideas the mentor should criticize:

- Incremental model swaps
- Underspecified "foundation model" claims
- Weak or saturated benchmarks
- Missing data provenance
- No ablation or failure analysis
- Domain claims without expert or real-world validation

### Honest Limits

Record:

- Evidence gaps
- Areas outside the scholar's public work
- Conflicting signals
- Time-sensitive claims needing refresh
- Sources that failed to download or required agent/browser fallback
