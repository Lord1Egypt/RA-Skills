## Description: <br>
An unofficial MCP server that lets agents access Vietnam stock market data, including current and historical prices, company financials, market statistics, and fund information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Vietnam stock, company, fund, gold price, exchange-rate, and quote data from the Xiaobenyang API after the user provides an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the Xiaobenyang API key in plaintext in a local .env file. <br>
Mitigation: Use a limited or disposable API key, restrict file access to the workspace, and delete the saved .env entry when the skill is no longer needed. <br>
Risk: Security evidence reports stale Gaokao identifiers that make the backend and credential scope unclear. <br>
Mitigation: Inspect the configured API endpoint, MCP identifiers, and credential scope before use, and confirm the requested key is appropriate for Vietnam market-data access. <br>
Risk: The security verdict is suspicious because the skill depends on an external API and local credential persistence. <br>
Mitigation: Install only if the user accepts sharing a Xiaobenyang API key with the service, and review dependency versions and network behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/alinklab/skills/vnstock) <br>
- [Xiaobenyang API key portal](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown summaries of JSON-backed API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY value; tool functions expose json, dataframe, and toon output formats where supported.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
