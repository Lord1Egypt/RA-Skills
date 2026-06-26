## Description: <br>
Generate detailed crypto tax reports for XPR Network activity with support for New Zealand and United States regional tax rules and cost basis methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulgnz](https://clawhub.ai/user/paulgnz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to compile XPR Network balances, DEX trades, transfers, rates, gains, income events, and Markdown/CSV tax-report outputs for supported NZ and US tax workflows. Reports are estimates and should be reviewed by a qualified tax professional before filing. <br>

### Deployment Geography for Use: <br>
New Zealand and United States <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports and CSVs may contain sensitive wallet-linked tax data and may be uploaded to external deliverable storage. <br>
Mitigation: Review storage and delivery destinations before use, avoid uploading data the user does not want stored externally, and confirm privacy handling for generated URLs. <br>
Risk: Tax estimates may be incomplete or jurisdiction-specific, especially around regional rules, tax-year boundaries, and unsupported activity types. <br>
Mitigation: Verify the selected jurisdiction, tax year, and cost-basis method, retain CSV exports for review, and have a qualified tax professional review the report before filing. <br>
Risk: Historical pricing can be limited or less accurate when CoinGecko access is unavailable or DEX-derived rates are sparse. <br>
Mitigation: Use a dedicated CoinGecko API key when needed and cross-check material rates or gaps before relying on the final report. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/paulgnz/xpr-tax) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3) <br>
- [CoinGecko Pro API](https://pro-api.coingecko.com/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown report plus CSV export data and structured tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only API queries and calculations; generated reports may contain wallet-linked tax data, balances, income events, and disposals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
