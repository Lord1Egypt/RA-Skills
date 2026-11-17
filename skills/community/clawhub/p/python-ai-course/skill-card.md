## Description:

Chinese-language AI full-stack tutoring skill that guides learners through personalized AI learning paths, assessments, practical Python examples, RAG, agents, model tuning, prompt engineering, and technology selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mxfwdream](https://clawhub.ai/user/mxfwdream)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, developers, and career-focused practitioners use this skill as a Chinese AI tutor to assess their level, build a structured AI full-stack study plan, practice with exercises, and receive implementation-oriented lessons and technology-selection guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad teaching triggers can turn short AI-learning questions into a fixed multi-step course workflow.

Mitigation: Deploy with user-facing expectations that the skill may ask assessment questions before teaching and may be better suited to structured learning than brief Q&A.

Risk: The skill can generate runnable Python examples and shell setup commands as part of lessons.

Mitigation: Have users review generated code and commands before execution, especially dependency installation, local file access, API use, or deployment steps.

Risk: The curriculum and vendor comparisons contain time-sensitive 2026 technology claims and product-positioning guidance.

Mitigation: Review and refresh current-topic and vendor-selection references periodically before relying on them for business or compliance decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mxfwdream/skills/python-ai-course)
- [Curriculum](references/curriculum.md)
- [Assessment bank](references/assessment_bank.md)
- [Lesson template](references/lesson_template.md)
- [Hot topics](references/hot_topics.md)
- [Agent comparison](references/agent_comparison.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with tables, exercises, answers, Python and shell code blocks, and visual-widget prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are conversational tutoring content tailored to learner level and AI topic.]

## Skill Version(s):

6.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
