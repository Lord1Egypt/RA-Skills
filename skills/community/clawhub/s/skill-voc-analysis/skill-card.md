## Description:

A general voice-of-customer (VOC) analysis skill that guides collection and organization of authentic customer feedback, categorizes themes, extracts critical-to-quality requirements, and suggests improvement priorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external teams, and analysts use this skill to turn user/customer feedback into categorized insights, CTQ candidates, improvement priorities, and review-ready reports. It is suited to complaint analysis, product improvement discovery, and service quality design when the feedback source remains user-provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer feedback supplied to the skill may contain sensitive or proprietary information.

Mitigation: Provide only feedback data intended for analysis and apply the deploying organization's data handling controls before use.

Risk: Incomplete or unverified feedback can lead to misleading categories, CTQ candidates, or improvement priorities.

Mitigation: Use the skill's confirmation gates for classification, CTQ conversion, and prioritization before acting on the report.

Risk: The artifact references optional guide, script, and asset files that are not included, which may limit automated report-building behavior.

Mitigation: Review the available artifact contents before relying on referenced automation, and use the conversational Markdown workflow or supply trusted supporting files where needed.

## Reference(s):

- [Server-resolved source repository](https://github.com/duding-engicool/skill-voc-analysis)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-voc-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Conversational analysis guidance with optional Markdown and HTML report outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided authentic feedback and user confirmation before CTQ and priority decisions.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter); release package version 0.1.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
