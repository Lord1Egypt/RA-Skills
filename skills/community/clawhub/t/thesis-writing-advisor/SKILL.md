---
name: thesis-writing-advisor
description: Generate complete undergraduate thesis topic, proposal, opening-report, and writing guidance from a user's research theme, population, variables, influencing factors, or preferred method. Use when users ask in Chinese or English for graduation thesis ideas, psychology thesis topics, undergraduate dissertation opening reports, proposal structure, literature-review plans, questionnaire designs, qualitative interview/case/focus-group designs, mixed-methods designs, non-empirical intervention-scheme papers, or chapter-by-chapter writing advice.
---

# Thesis Writing Advisor

## Overview

Use this skill to turn a user's rough undergraduate thesis idea into a defensible topic, research design, opening-report outline, and chapter-by-chapter writing guide. Default to Chinese when the user asks in Chinese.

Focus especially on psychology undergraduate work, while adapting the workflow to adjacent education, counseling, social science, and student-development topics.

## First Response Workflow

1. Extract the user's supplied research theme, research content, population, phenomenon/variables, influencing factors, method preference, available data/materials, data constraints, and school requirements.
2. If key information is missing but a reasonable assumption is safe, state the assumption and proceed. Ask at most one concise question only when the choice would materially change the design.
3. Identify the best paper type:
   - Empirical questionnaire study
   - Literature review or systematic/scoping review
   - Intervention-scheme design paper
   - Theoretical analysis paper
   - Qualitative interview, focus-group, case-study, phenomenological, ethnographic, narrative, document-analysis, or grounded-theory study when the user can collect suitable textual/observational material
   - Mixed-methods study when quantitative results and qualitative explanation are both needed and feasible
4. Produce one recommended topic plus 3-5 alternate topic titles.
5. Give a complete writing guide: research background, research content, research questions, variables or qualitative concepts, methods, participants/materials, tools or protocols, analysis/evaluation plan, chapter outline, chapter-by-chapter continuation plan, expected innovation, feasibility, limitations, and cautions.
6. Clearly distinguish what the paper can conclude from what requires future empirical verification.

## Method Selection Rules

Prefer simple, feasible designs for undergraduate users:

- Use questionnaire survey + correlation/regression when the user can collect data and mentions variables or influencing factors.
- Use intervention-scheme design when the user does not want to implement an intervention or collect effect data but wants an applied psychology design.
- Use literature review/systematic review when the user cannot collect data and the school allows non-empirical theses.
- Use theoretical analysis when the topic is concept-heavy and not suited to basic survey measurement.
- Use qualitative design when the user's purpose is deep understanding of lived experience, meaning, process, culture, context, or a bounded case rather than variable testing.
- Use mixed methods only when each method answers a distinct part of the research question and the user can handle both data streams.

When the user says they will not collect or analyze data, avoid wording such as "effect study", "experimental study", or "empirical test". Use "scheme design", "mechanism analysis", "literature review", or "application research".

## Qualitative and Mixed Methods Pattern

When the user mentions interview, focus group, observation, document analysis, case study, phenomenology, ethnography, grounded theory, narrative analysis, discourse analysis, or mixed methods, read `references/qualitative-methods.md`.

For qualitative designs, make the output concrete:

1. Purpose: describe what experience, meaning, case, process, culture, or theory the study seeks to understand.
2. Research content: break the user's topic into 3-5 concrete study contents or tasks.
3. Research questions: use open "how/what" questions, not causal hypotheses.
4. Participants/materials: specify purposive sampling, inclusion criteria, sample size range, and data sources.
5. Collection: give an interview/focus-group/observation/document protocol plan, consent, confidentiality, recording, and transcription.
6. Analysis: explain coding, category/theme development, constant comparison, cross-case analysis, or theory generation as appropriate.
7. Trustworthiness: include triangulation, reflexivity, member checking/participant verification where feasible, thick description, and audit trail.
8. Chapters: include a draftable thesis chapter structure and what the user should add to each chapter.
9. Limits: avoid broad statistical generalization; frame findings as contextual, transferable, or theory-building.

## Psychology Intervention-Scheme Pattern

For non-implemented intervention papers, frame the work as "psychological intervention scheme development/design", not intervention efficacy research.

Use this standard logic:

1. Problem background: define the target issue and why it matters.
2. Literature basis: summarize mechanisms, risk factors, and existing interventions.
3. Theory model: map the issue into a practical mechanism model.
4. Intervention targets: convert the theory model into general and specific goals.
5. Scheme design: specify population, inclusion/exclusion, format, number of sessions, duration, implementer, materials, ethics, and risk referral.
6. Session plan: give a table of session number, theme, goal, content, and homework/practice.
7. Evaluation plan: explain how future implementation could test feasibility and effects.
8. Limitation: state that no direct effectiveness conclusion can be drawn without implementation data.

For detailed templates and wording, read `references/psychology-thesis-guide.md`.

When the user wants example papers, literature-based examples, or models to imitate, read `references/sample-papers.md` and convert the relevant studies into thesis topic examples, methods, and chapter-writing guidance.

When the user asks for a complete thesis plan, opening-report-to-thesis path, or content they can keep expanding into a full paper, read `references/chapter-plans.md` and include a "毕业论文可续写章节规划" section.

## Output Standards

Include concrete, thesis-ready wording whenever useful:

- Topic title variants
- Research purpose and significance
- Research questions or hypotheses
- Research content decomposed into concrete tasks
- Variable definitions and likely scales
- Method section wording
- Qualitative or mixed-methods design wording when relevant
- Opening-report structure
- Chapter outline
- Chapter-by-chapter continuation plan with section headings, writing tasks, and materials the user should add next
- Schedule or technical route
- Risk, ethics, and feasibility notes

Keep recommendations realistic for an undergraduate timeline. Warn when a design is too broad, ethically sensitive, clinically high-risk, or likely to be rejected by schools requiring empirical data.

## Source Handling

When the user asks for online search, latest literature, exact references, scales, policy requirements, or source links, browse and cite credible sources. Prefer official frameworks, academic databases, peer-reviewed articles, and recognized reporting guidelines. Do not invent citations.
