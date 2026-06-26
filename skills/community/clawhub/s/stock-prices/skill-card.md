## Description: <br>
Query real-time stock prices and market data using the Stock Prices API, with responses returned in TOON format for decoding by @toon-format/toon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anthonylee1994](https://clawhub.ai/user/anthonylee1994) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch current quote data for one or more stock symbols, then decode the TOON response for price monitoring, portfolio tracking, or market summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols are sent to the disclosed stock-prices.on99.app service. <br>
Mitigation: Use the skill only when sharing requested symbols with that service is acceptable. <br>
Risk: The optional TOON decoder adds a project dependency. <br>
Mitigation: Install @toon-format/toon deliberately and prefer a pinned package version. <br>


## Reference(s): <br>
- [Stock Prices on ClawHub](https://clawhub.ai/anthonylee1994/stock-prices) <br>
- [anthonylee1994 publisher profile](https://clawhub.ai/user/anthonylee1994) <br>
- [Stock Prices API endpoint](https://stock-prices.on99.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses from the disclosed API are TOON text and should be decoded before structured use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
