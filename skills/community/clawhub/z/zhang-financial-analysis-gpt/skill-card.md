## Description:

将“张氏财务分析框架”落地为可直接执行的查表、计算、判断与排雷步骤，帮助使用者依据财务报表和附注识别利润含金量、产业链话语权、潜在雷区、集团管控模式与管理效能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiyouwolegequ](https://clawhub.ai/user/aiyouwolegequ)

### License/Terms of Use:

MIT-0

## Use Case:

Financial analysts, investors, credit reviewers, operators, and advisors use this skill to turn Chinese financial statements, notes, and group-level reporting data into plain-language diagnostics for profit quality, cash conversion, asset risks, operating leverage, and parent-subsidiary structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial analysis may be mistaken for audit, legal, or investment advice.

Mitigation: Use outputs for screening and business-risk analysis only, and require qualified review before relying on conclusions for audit, legal, credit, or investment decisions.

Risk: Incomplete financial statements, missing notes, single-year data, or absent industry context can lead to overconfident conclusions.

Mitigation: Ask users to provide cash-flow data, balance-sheet detail, notes and disclosures, multi-year periods, industry context, and parent-company statements when available; clearly mark conclusion boundaries when data is missing.

Risk: Non-public financial data may be sensitive.

Mitigation: Use the skill only in trusted environments and avoid supplying confidential data where retention, access, or sharing controls are unclear.

Risk: The skill defaults to Chinese plain-language output, which may not fit every user.

Mitigation: Ask for the preferred language or adapt the output language when Chinese is unsuitable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiyouwolegequ/skills/zhang-financial-analysis-gpt)
- [ClawHub publisher profile](https://clawhub.ai/user/aiyouwolegequ)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Markdown or structured text with financial calculations, risk labels, conclusions, and missing-data boundaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese plain-language financial analysis; reliability depends on supplied statements, notes, period coverage, industry context, and parent-company data.]

## Skill Version(s):

2.0.0 (source: server release metadata and target metadata; artifact frontmatter lists 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
