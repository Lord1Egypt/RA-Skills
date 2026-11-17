## Description:

Generate detailed crypto tax reports for XPR Network activity with support for New Zealand and United States regional tax rules and cost basis methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgnz](https://clawhub.ai/user/paulgnz)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to gather XPR Network balances, DEX trades, transfers, rates, and generated tax report artifacts for NZ or US crypto tax workflows. The outputs are estimates and should be reviewed with a tax professional before filing or financial reliance.

### Deployment Geography for Use:

New Zealand and United States

## Known Risks and Mitigations:

Risk: Generated tax reports and CSVs may contain sensitive financial records and are externally delivered.

Mitigation: Confirm where deliverables are stored, whether URLs are public or permanent, and require explicit user approval before uploading reports or CSV exports.

Risk: Tax calculations are estimates and may not be suitable as filed tax advice.

Mitigation: Preserve the generated disclaimer and have a qualified tax professional verify calculations before relying on them.

Risk: Generated CSV files may be unsafe when opened in spreadsheet software.

Mitigation: Treat CSV exports as untrusted files and review or sanitize them before opening in spreadsheet applications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulgnz/skills/xpr-tax)
- [ClawHub publisher profile](https://clawhub.ai/user/paulgnz)
- [CoinGecko API](https://api.coingecko.com/api/v3)
- [CoinGecko Pro API](https://pro-api.coingecko.com/api/v3)

## Skill Output:

**Output Type(s):** [text, markdown, csv, configuration, guidance]

**Output Format:** [JSON tool results, Markdown tax reports, and CSV export content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries external APIs for read-only XPR Network data and may require COINGECKO_API_KEY for complete historical pricing.]

## Skill Version(s):

1.0.0 (source: server evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
