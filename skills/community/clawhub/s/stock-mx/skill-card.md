## Description: <br>
Stock gives agents natural-language access to Eastmoney Miaoxiang financial news search, stock screening, and market, financial, relationship, and company data queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jade-srgb](https://clawhub.ai/user/Jade-srgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current financial information, screen stocks from natural-language criteria, and format returned securities data for analysis. It is intended for financial research and data retrieval workflows that need fresher external data than model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact publishes and directs use of a shared fallback API key for external financial API requests. <br>
Mitigation: Configure a user-controlled MX_APIKEY through a secure environment or secret store and avoid relying on the bundled default key. <br>
Risk: Financial queries are sent to an external financial API. <br>
Mitigation: Avoid including private account, portfolio, trading-plan, or confidential research details in prompts. <br>
Risk: Large historical data requests can produce very large responses. <br>
Mitigation: Scope requests by security, metric, and time range before querying to reduce context overload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jade-srgb/stock-mx) <br>
- [Artifact overview](artifact/SKILL.md) <br>
- [Financial data skill reference](artifact/mx_data.md) <br>
- [Financial news search skill reference](artifact/mx_search.md) <br>
- [Stock screening skill reference](artifact/mx_select_stock.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown summaries with JSON-derived tables, CSV-style stock data, and inline curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include financial-news summaries, stock-screening tables, securities metadata, indicator descriptions, and prompts to use a secure MX_APIKEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
