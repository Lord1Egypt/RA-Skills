## Description:

Quantitative analysis skill for the Chinese A-share market using Tushare Pro data and a holiday helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-wu66](https://clawhub.ai/user/noah-wu66)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to query and interpret Chinese A-share securities data, screen stocks, diagnose individual securities, check market calendars, and combine Tushare data with event research when judgment is requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Tushare API token for most bundled scripts.

Mitigation: Provide the token through the configured environment secret path and avoid committing or pasting it into shared files.

Risk: Recommendation-style analysis can be incorrect, stale, or incomplete.

Mitigation: Verify cited sources and numeric outputs independently, and treat the response as decision support rather than financial advice.

Risk: User-requested exports can create or overwrite local files.

Mitigation: Use output paths intentionally and review paths before running commands with --output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noah-wu66/skills/quant-expert)
- [Tushare Pro API Quick Reference](references/api_quick_reference.md)
- [Quantitative Analysis Strategies](references/analysis_strategies.md)
- [timor.tech Holiday API](https://timor.tech/api/holiday/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional shell commands, tables, CSV exports, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Tushare and holiday API network queries; optional file exports are user-requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
