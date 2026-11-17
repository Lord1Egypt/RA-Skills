## Description:

VC投资筛选工具 uses a four-layer assessment flow across macro policy, industry trends, sub-sector selection, and company fundamentals to support investment screening and company evaluation for angel, VC, growth, and M&A stages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksyooh](https://clawhub.ai/user/ksyooh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and investment teams use this skill to collect investment preferences, screen venture sectors, evaluate companies, create investment reports, and revisit prior analyses. It is most applicable to China-market VC research that relies on policy, industry, financing, company, and public-market data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores user-linked investment preferences, report indexes, cached API results, and investment reports across sessions.

Mitigation: Review retention expectations before installation, keep persistent files in controlled workspaces, and require documented deletion or retention controls for production use.

Risk: The skill can upload generated reports to Feishu and may include sensitive investment research or user context.

Mitigation: Confirm Feishu destination, permissions, and data classification before enabling archival workflows or sharing generated reports.

Risk: The skill uses configured business-data API credentials and also supports credential fallback from local memory files.

Mitigation: Prefer environment-managed credentials, restrict credential-file access, and avoid installing unless credential handling is acceptable for the deployment.

Risk: The skill performs network calls to business-data and public data sources, including configurable People Data base URLs.

Mitigation: Pin and review allowed API hosts, monitor outbound requests, and validate source attribution in generated investment conclusions.

Risk: Investment analysis may be incomplete or misleading when paid APIs are unavailable and the skill falls back to public data or web search.

Mitigation: Require source labels, confidence levels, and human review before using outputs for investment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ksyooh/skills/vc-investment-scout)
- [Data Capability and Fallback Strategy](artifact/references/data-capability.md)
- [Macro Data Source Reference](artifact/references/data-sources.md)
- [Investment Screening Methodology](artifact/references/methodology.md)
- [Company Evaluation Template](artifact/references/evaluation-template.md)
- [User Preference Questions](artifact/references/phase0-questions.md)
- [User-Provided Methodology Framework](artifact/references/user-methodology.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, narrative analysis, scoring matrices, source labels, confidence statements, and occasional JSON from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist user preferences, report indexes, cached API results, and archived investment reports across sessions.]

## Skill Version(s):

1.4.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
