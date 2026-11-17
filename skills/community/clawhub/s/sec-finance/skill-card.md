## Description:

Fetch structured financial data and filing metadata from SEC EDGAR and SEC XBRL companyfacts for US-listed companies, especially Chinese issuers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangwllu](https://clawhub.ai/user/wangwllu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to resolve SEC CIKs, fetch companyfacts data, and return quarterly or annual revenue, net income, EPS, and filing metadata. It is intended for structured SEC data retrieval, not investor-relations PDF discovery or downloading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic relaxed SSL fallback can allow tampered SEC data to be accepted on a hostile or misconfigured network.

Mitigation: Review before installing, independently verify financial outputs, and remove or disable relaxed SSL fallback before relying on the skill for decision-grade results.

## Reference(s):

- [SEC XBRL companyfacts API](https://data.sec.gov/api/xbrl)
- [SEC EDGAR company search](https://www.sec.gov/cgi-bin/browse-edgar)
- [Issuer CIK reference data](references/issuers.json)
- [ClawHub skill page](https://clawhub.ai/wangwllu/skills/sec-finance)
- [Publisher profile](https://clawhub.ai/user/wangwllu)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands]

**Output Format:** [Plain text table or JSON, typically summarized for the user in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include resolved CIK, company name, filing form, period end, revenue, net income, EPS, currency, concepts used, and SEC data update timestamp.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
