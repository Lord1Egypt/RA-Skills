---
name: thesis-discussion-writer
description: Write detailed, academically rigorous Chinese discussion chapters or discussion sections for theses, dissertations, and undergraduate papers from a user's findings, research questions, hypotheses, themes, theoretical framework, literature review, limitations, implications, and extra information. Use when users ask to write, expand, polish, organize, or structure only the Discussion/Chapter Five/第五章讨论/总结与讨论/讨论与结论 section, including summary of the study, discussion of findings, theoretical and literature interpretation, unexpected results, practical implications, recommendations for future research, and conclusions.
---

# Thesis Discussion Writer

## Scope

Use this skill only to write the discussion part of a Chinese academic paper. The default output is a polished Chinese "第五章 讨论" or "第五章 总结、讨论与结论" section.

Do not write new results, methodology, literature review, questionnaire design, or full thesis chapters outside the discussion scope. The discussion chapter interprets results already reported elsewhere; it should not introduce new data, new statistical analyses, new interview excerpts, or unsupported conclusions.

## Required Reference

Before drafting a full discussion chapter, read `references/discussion-writing-guide.md`. It contains chapter structures, finding-by-finding discussion rules, theory/literature integration patterns, implications, recommendations, conclusions, Chinese templates, and quality checks derived from the local `5discussion.txt` source.

## Input Extraction

Extract and use any information the user provides:

- Thesis title, discipline, research problem, purpose, and chapter naming requirement
- Research questions, hypotheses, variables, qualitative themes, cases, or mixed-methods strands
- Main findings from the Results chapter, including significant and non-significant results
- Theoretical framework, conceptual model, or epistemological framework
- Prior studies or literature review points that should be compared with the findings
- Method design, sample, instruments, data sources, and analysis limitations
- Unexpected findings, possible explanations, confounding factors, mediators, or contextual factors
- Practical audience: students, teachers, counselors, parents, managers, policymakers, institutions, or researchers
- School requirements for sections such as "研究总结", "结果讨论", "实践启示", "研究不足与展望", and "结论"

If the user has not provided actual findings, do not invent conclusions, implications, literature comparisons, or recommendations. Provide a discussion-chapter framework with placeholders and a list of exact materials needed.

## Discussion Type Decision

Infer the best discussion pattern before writing:

- Quantitative: discuss each research question, hypothesis, variable, relationship, group difference, regression model, or non-significant result in the same order as the Results chapter.
- Qualitative: discuss themes, cases, participant experiences, cross-case patterns, theoretical insights, and transferability while staying close to the qualitative data.
- Mixed methods: discuss quantitative and qualitative findings separately or integrate them by research question, explaining convergence, divergence, and complementarity.
- Literature review/systematic review: discuss evidence patterns, conceptual contributions, literature gaps, methodological limitations, and implications for future research.
- Intervention-scheme design without implementation: discuss theoretical rationale, feasibility, expected application value, risk controls, evaluation plan, and limitations; do not claim effectiveness.

## Drafting Workflow

1. Identify the study type and the chapter format expected by the user's school.
2. Start with a brief introduction/advance organizer for the discussion chapter.
3. Summarize the study briefly: problem, purpose, framework, research questions/method, and major findings.
4. Discuss findings one by one, following the same order as the Results chapter.
5. For each finding, explain what it means, connect it to theory and literature, and state whether it supports, contradicts, or extends existing knowledge.
6. Explain unexpected or weak results through sampling, instrumentation, research design, context, or unmeasured variables when evidence permits.
7. Derive practical implications directly from findings and match them to concrete stakeholders.
8. Derive future research recommendations from findings, limitations, unanswered questions, and methodological constraints.
9. End with conclusions that make defensible assertions based on the findings, without adding new data.

## Output Standards

For a full discussion chapter, include:

- Complete Chinese draft with numbered headings
- A short study summary when the requested chapter includes it
- Finding-by-finding discussion organized by research question, hypothesis, variable, theme, case, or model
- Integration with theory and literature when the user supplies enough context
- Explanation of unexpected findings and plausible limitations when relevant
- Practical implications grounded in results
- Recommendations for future research grounded in results and limitations
- Conclusions that synthesize the whole study

Quality requirements:

- Stay close to the data.
- Do not overgeneralize beyond the sample, data source, method, or design.
- Do not repeat technical statistics already reported in the Results chapter unless needed for clarity.
- Do not turn recommendations into unsupported claims.
- Do not write implications that are broader than the findings can support.
- Do not introduce new analyses or new evidence in the Discussion chapter.
- Preserve limitations and uncertainty instead of forcing strong conclusions.
