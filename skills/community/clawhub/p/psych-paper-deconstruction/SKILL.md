---
name: psych-paper-deconstruction
description: "心理学文献精读拆解助手。输入心理学论文（PDF/Word/文本），自动梳理研究假设、实验范式、自变量因变量、统计方法、研究局限与现实现实引申等结构化分析，输出可直接用于专业课作业的精读报告。触发词：精读论文、拆解文献、分析心理学论文、paper deconstruction、文献精读、论文拆解、实验范式分析。This skill should be used when a user provides a psychology research paper and wants a structured close-reading analysis covering hypotheses, experimental design, variables, statistics, limitations, and practical implications. Suitable for applied psychology coursework assignments."
---

# 心理学文献精读拆解助手

## Overview

This skill provides a systematic workflow for deconstructing psychology research papers into structured analysis reports. Given a psychology paper (PDF, Word, or plain text), produce a comprehensive close-reading report that covers research hypotheses, experimental paradigms, independent/dependent variables, statistical methods, limitations, and practical implications — formatted for direct use in applied psychology course assignments.

## Input Handling

Accept papers in the following formats:

1. **PDF files** — Use the Read tool to extract text. If the PDF is scanned or image-based, use OCR if available; otherwise inform the user and request a text version.
2. **Word documents (.docx)** — Use the Read tool or appropriate document processing tools to extract content.
3. **Plain text / pasted content** — Process directly.
4. **Web links to papers** — Use WebFetch to retrieve the abstract and available content; note that full-text access may be limited.

After extracting the paper content, confirm the paper title and authors with the user before proceeding to analysis.

## Analysis Workflow

Execute the following steps in sequence to produce the deconstruction report.

### Step 1: Extract Basic Information

Identify and record:
- Paper title (original language + Chinese translation if applicable)
- Authors and affiliations
- Journal name, volume, issue, year
- DOI or other identifiers
- Keywords listed by the authors

### Step 2: Locate Research Background & Question

Extract:
- The broader research context the paper situates itself in
- The specific research gap or problem being addressed
- The main research question(s)

Distinguish between what the authors explicitly state and what can be inferred. Label inferences clearly with "[推断]".

### Step 3: Identify Research Hypotheses

Extract all stated hypotheses (H1, H2, H3, ...). For each hypothesis:
- Quote the original statement
- Identify the direction (directional vs. non-directional)
- Map which variables it connects
- Note whether each hypothesis is a priori (pre-registered) or appears post-hoc

If hypotheses are not explicitly stated, reconstruct them from the research questions and predictions, labeling them as "[重构假设]".

### Step 4: Analyze Research Design

Determine and document:
- **Design type**: between-subjects, within-subjects, mixed, correlational, longitudinal, case study, meta-analysis, etc.
- **Experimental vs. observational**: Is this a true experiment, quasi-experiment, or observational study?
- **Number of conditions/groups**
- **Random assignment**: Was random assignment used? What was the unit of randomization?
- **Control conditions**: What serves as the control/baseline?

Consult `references/psychology_research_methods.md` for design-type definitions and decision criteria.

### Step 5: Identify Experimental Paradigm

Identify the experimental paradigm or task used:
- Is it a well-established paradigm (e.g., Stroop, Simon, Flanker, N-back, Posner cueing, IAT, dot-probe, lexical decision, go/no-go)?
- Is it a novel/adapted paradigm? Describe the task structure.
- What are the trial-level events and timings?
- What stimuli are used?

Consult `references/psychology_research_methods.md` → "Common Experimental Paradigms" section for a catalog of established paradigms and their characteristics.

### Step 6: Extract Variables

Create a structured variable table:

**Independent Variables (IVs):**
| Variable | Levels | Type (manipulated/subject) | Operationalization |
|----------|--------|----------------------------|---------------------|
| ...      | ...    | ...                        | ...                 |

**Dependent Variables (DVs):**
| Variable | Measurement Type | Scale | Unit |
|----------|-----------------|-------|------|
| ...      | ...             | ...   | ...  |

**Control / Covariate Variables:**
List all variables held constant or used as covariates (e.g., age, gender, education level, IQ, mood state).

If operationalization is ambiguous, note it with "[操作化不明确]" and suggest a clearer definition.

### Step 7: Identify Statistical Methods

Document:
- Descriptive statistics used
- Inferential tests (t-test, ANOVA, ANCOVA, regression, mediation/moderation, SEM, etc.)
- Significance level (α)
- Effect size measures reported (Cohen's d, η², partial η², r, OR, etc.)
- Corrections for multiple comparisons (Bonferroni, FDR, etc.)
- Software used (SPSS, R, Python, etc.)

If advanced or unusual methods are used, briefly explain what they test.

### Step 8: Summarize Main Results

For each hypothesis:
- State whether it was supported, partially supported, or rejected
- Report key statistics (test statistic, p-value, effect size)
- Describe the direction and magnitude of effects
- Note any unexpected or null findings

Organize results by hypothesis, not by analysis order, to maintain coherence.

### Step 9: Analyze Limitations

Identify limitations from two sources:
1. **Author-stated limitations** — Quote or closely paraphrase from the Discussion section.
2. **Critically identified limitations** — Assess:
   - **Internal validity**: confounds, demand characteristics, experimenter effects, history/maturation/attrition threats
   - **External validity**: sample representativeness, ecological validity, generalizability
   - **Construct validity**: operationalization adequacy, face/construct validity of measures
   - **Statistical validity**: power adequacy, multiple comparison issues, assumption violations
   - **Ethical considerations**: informed consent, debriefing, potential for harm

Label author-stated limitations vs. critically identified ones.

### Step 10: Extract Practical Implications

Document:
- **Theoretical contributions**: How does this study advance theory? Does it support, challenge, or extend existing models?
- **Applied/practical implications**: What real-world applications does the study suggest? (clinical, educational, organizational, consumer, etc.)
- **Future research directions**: What do the authors recommend? What additional questions does the analysis reveal?

### Step 11: Critical Evaluation

Provide a balanced critical assessment:
- **Strengths**: methodological rigor, novelty, theoretical contribution
- **Weaknesses**: design flaws, measurement issues, generalizability concerns
- **Overall assessment**: Rate the study's contribution on a scale (moderate / substantial / significant) with justification

### Step 12: Generate Output

Format the complete analysis using the template in `assets/analysis_template.md`. Produce the report in Markdown. Offer to also export as a Word document if the user needs it for assignment submission.

## Output Format

The final report must follow this structure (see `assets/analysis_template.md` for the full template):

1. 论文基本信息
2. 研究背景与问题
3. 研究假设
4. 研究设计
5. 实验范式
6. 变量分析（自变量 / 因变量 / 控制变量）
7. 统计方法
8. 主要结果
9. 研究局限
10. 现实引申
11. 批判性评价
12. 参考格式（APA 格式引用）

## Quality Standards

- **Accuracy**: All statistics and findings must be traceable to the original paper. Never fabricate or infer data points.
- **Completeness**: Cover all 12 sections. If a section is not applicable (e.g., no explicit hypotheses), state so explicitly rather than omitting.
- **Clarity**: Use plain language. Define technical terms on first use. Assume the reader is an undergraduate psychology student.
- **Honesty**: Clearly distinguish between what the authors stated and what the analysis infers. Use labels: [原文], [推断], [重构假设], [操作化不明确].
- **APA formatting**: Use APA 7th edition style for any in-text citations and the reference entry.

## References

- `references/psychology_research_methods.md` — Catalog of common experimental paradigms, research designs, statistical methods, and validity threat checklists. Consult this when identifying design types, paradigms, or validity issues.
- `assets/analysis_template.md` — Output template for the final deconstruction report. Use this as the structural basis for the generated report.
