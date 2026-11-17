## Description:

Routes advertising account operations, supported campaign workflows, and market-analysis and reporting tasks through Siluzan TSO for Google, Bing, Yandex, TikTok, and Meta.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sigedev01-bit](https://clawhub.ai/user/sigedev01-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Advertising operators and marketing analysts use this skill to inspect accounts, carry out supported campaign operations, and prepare platform or market-analysis reports. Campaign creation workflows are documented for Google and Meta.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional installers can make broad, lasting changes to the environment.

Mitigation: Prefer manual installation into one assistant directory, preserve the existing npm registry, and install Node separately.

Risk: Account changes can affect live campaigns and budgets.

Mitigation: Require explicit approval of target accounts, budgets, live activation, and deletions before those actions.

Risk: Onboarding or uploads can expose identity, banking, or customer data.

Mitigation: Use protected onboarding for identity and banking details, and authorize customer-data sharing before uploads.

## Reference(s):

- [Siluzan TSO on ClawHub](https://clawhub.ai/sigedev01-bit/skills/siluzan-tso)
- [Intent routing](references/core/intent-routing.md)
- [Workflows](references/core/workflows.md)
- [Google Ads write workflows](references/google-ads/google-ads-write.md)
- [Report templates](references/report-templates/README.md)
- [Setup](references/core/setup.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, HTML reports, Spreadsheets, JSON configuration, Shell commands]

**Output Format:** [Markdown, HTML, XLSX, JSON, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output formats and schemas vary by workflow; campaign and report outputs use documented templates.]

## Skill Version(s):

1.1.65 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
