## Description:

Produces cited supplier due-diligence and delivery-capacity reports for one or two companies using procurement records and public information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement teams and buyers use the skill to review a supplier's bidding history, customer relationships, and cited public risk information, or to compare two prospective suppliers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trial registration collects a hashed device identifier.

Mitigation: Require explicit consent before registration; manually configure ZLBX_API_KEY to skip it.

Risk: An automatically issued API key may be saved in the user's home directory.

Mitigation: Review local credential storage before installation and restrict access to the saved key.

Risk: Exported reports can expose signed no-login links to anyone who receives them.

Mitigation: Share reports only with intended recipients and review links before distribution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhiliaobiaoxun/skills/supplier-qualification-checker)
- [Workflow guide](references/workflow.md)
- [API reference](references/api-quick.md)
- [Registration and privacy guidance](references/auto-register.md)
- [Report templates](references/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML reports]

**Output Format:** [Markdown response and shareable HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports cite source records; shared HTML may contain signed no-login links.]

## Skill Version(s):

1.0.6 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
