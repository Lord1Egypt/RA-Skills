## Description:

RiskBlind Radar is a Chinese-language decision-risk prompting skill that proactively asks overlooked risk questions before a user makes plans, commitments, or budget decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryuutora1986](https://clawhub.ai/user/ryuutora1986)

### License/Terms of Use:

MIT-0

## Use Case:

External users, independent founders, small-team leads, and heavy AI assistant users use this skill to have an agent challenge plans, assumptions, budgets, commitments, and opportunity signals with concise risk-oriented follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may frequently challenge plans, commitments, budgets, and assumptions in Chinese when trigger phrases match.

Mitigation: Review and narrow the trigger phrases if the deployment should avoid frequent risk-oriented follow-up questions.

Risk: The optional observation log can store local notes about unresolved risks or commitments.

Mitigation: Enable local observation logging only when users are comfortable storing those notes, and avoid recording sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryuutora1986/skills/riskblind-radar)
- [README](artifact/readme.md)
- [Question templates](artifact/question_templates.md)
- [Risk and cognitive-bias rules](artifact/rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style natural-language questions and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces at most two risk-oriented follow-up questions per turn and may reference optional local observation notes when enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
