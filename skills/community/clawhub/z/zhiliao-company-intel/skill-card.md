## Description:

Produces company background reports and two-company comparisons grounded in public procurement records, including customer relationships, awards, competitors, and cited public-risk information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

Business users, procurement teams, and sales teams assess a company's bidding history, customer and supplier relationships, and competitors, or compare two companies before making business decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional trial signup sends the operating system, CPU architecture, and a hashed MAC identifier to the vendor for quota deduplication.

Mitigation: Ask for explicit consent before signup; use an existing API key or decline the trial to avoid device-data submission.

Risk: The API key may be stored in a local configuration file.

Mitigation: Protect access to the local credential file and do not include the key in reports or conversation output.

Risk: Contact lookup could expose information about individuals.

Mitigation: Use contact lookup only for legitimate business purposes and mask contact details in reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhiliaobiaoxun/skills/zhiliao-company-intel)
- [Vendor skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [API quick reference](references/api-quick.md)
- [Company intelligence workflow](references/workflow.md)
- [Report templates](references/report-template.md)
- [Trial signup and credential setup](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML files]

**Output Format:** [Markdown report in the conversation and a shareable local HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports a single-company report or a two-company comparison; cites source links and identifies data gaps.]

## Skill Version(s):

1.0.6 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
