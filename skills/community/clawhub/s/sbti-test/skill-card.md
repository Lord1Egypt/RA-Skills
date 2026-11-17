## Description:

SBTI is an entertainment personality-test skill that interactively collects multiple-choice answers and returns a structured report on personality dimensions, type, interpersonal suggestions, and career-fit considerations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biggodcheng](https://clawhub.ai/user/biggodcheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for entertainment-oriented self-exploration by answering a guided SBTI questionnaire and receiving a structured personality report. The report can support reflection about interpersonal style and career preferences, but it is not a psychological diagnosis or sole basis for career decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks personal, provocative Chinese-language personality and relationship questions.

Mitigation: Install and run it only when users are comfortable answering those questions, and present participation as optional.

Risk: Users may over-rely on personality or career interpretations.

Mitigation: Treat the generated report as entertainment and self-reflection, not psychological, medical, or career decision advice.

Risk: Broad personality-test triggers may activate the skill unintentionally.

Mitigation: Invoke it with explicit SBTI wording and avoid using generic personality-test phrasing when another workflow is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biggodcheng/skills/sbti-test)
- [README_EN.md](artifact/README_EN.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown personality assessment report with dimension scores, personality type summary, strengths and weaknesses, and interpersonal or career suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated from user-selected questionnaire answers; results should be treated as entertainment and self-reflection rather than professional advice.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
