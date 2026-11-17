## Description:

Searches Xiaohongshu posts by keyword, date range, and popularity, returns engagement data and report exports, and can coordinate a credit recharge when the API balance is insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users can search Xiaohongshu posts by keyword, date range, and sort order, then review structured post and engagement data. They can also request CSV and HTML reports for offline review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to RedFox.

Mitigation: Avoid sending confidential or sensitive queries.

Risk: Recharge setup may install payment software and initiate a payment.

Mitigation: Require approval before installation or recharge setup, verify the recipient and amount, and use a reviewed, pinned installer.

Risk: Shell and report-export handling requires fixes; retrieved content may be handled in ways that can execute commands or browser code.

Mitigation: Wait until shell and report-export handling is fixed before using exports.

## Reference(s):

- [Alipay recharge workflow](references/alipay-recharge.md)

## Skill Output:

**Output Type(s):** [Markdown, CSV files, HTML reports]

**Output Format:** [Markdown results table, with optional CSV and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches accept a keyword and optional date range and sort order; report exports are optional.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
