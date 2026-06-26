## Description: <br>
Official Supermetrics skill. Query marketing data from 100+ platforms including Google Analytics, Meta Ads, Google Ads, and LinkedIn. Requires API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bartschneider](https://clawhub.ai/user/bartschneider) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing analysts, developers, and agents use this skill to discover Supermetrics data sources, accounts, fields, and query results from connected advertising and analytics platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query Supermetrics-connected marketing accounts using an API key. <br>
Mitigation: Use a scoped or revocable API key where possible and confirm the target account, fields, and date range before running queries. <br>
Risk: Filters or search text could expose unrelated sensitive information to the Supermetrics API. <br>
Mitigation: Avoid placing unrelated secrets or confidential text in filters, search queries, or query parameters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bartschneider/supermetrics-openclawd) <br>
- [Supermetrics MCP endpoint](https://mcp.supermetrics.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and JSON response objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUPERMETRICS_API_KEY and returns success/error JSON dictionaries from API helper functions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
