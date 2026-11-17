## Description:

Audits third-party agent skills before installation and explains potential security risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users submit authorized skill files for a pre-installation security audit and review findings before deciding whether to install or enable the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted skill files are sent to a hosted audit service and may contain confidential content.

Mitigation: Submit only authorized files; remove secrets, personal data, and proprietary material before auditing.

Risk: An exposed or overprivileged API key could allow unauthorized use of the audit service.

Mitigation: Use a least-privilege key where possible and keep it out of chat, submitted files, logs, and reports.

Risk: An incomplete audit or a review-required result could be mistaken for approval to install.

Mitigation: Allow automated installation only after a complete, parseable pass; stop on errors or blocks and request human review for review results.

## Reference(s):

- [SkillGuard release on ClawHub](https://clawhub.ai/youteacher/skills/skillguard)
- [AI Skills platform](https://ai-skills.open-idea.net)
- [API key configuration](https://ai-skills.open-idea.net/skill-docs/skillguard/API-KEY.md)
- [Audit workflow](https://ai-skills.open-idea.net/skill-docs/skillguard/AUDIT-WORKFLOW.md)
- [HTTP requests and responses](https://ai-skills.open-idea.net/skill-docs/skillguard/HTTP-REQUESTS.md)
- [Behavior and decision rules](https://ai-skills.open-idea.net/skill-docs/skillguard/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown audit summary and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes findings, risk level, and next steps from the audit response.]

## Skill Version(s):

1.7.0 (source: SKILL.md metadata.packageVersion, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
