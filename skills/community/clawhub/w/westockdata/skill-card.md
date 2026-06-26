## Description: <br>
Queries Tencent WeStock public market data for A-share, Hong Kong, and U.S. stocks, indexes, sectors, ETFs, financial reports, fund flows, technical indicators, shareholder data, dividends, calendars, IPOs, and related market views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[westock-skills](https://clawhub.ai/user/westock-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial-data researchers, quant developers, investor education teams, and market analysts use this skill to fetch and compare structured public market data across A-share, Hong Kong, and U.S. markets. It supports data retrieval and presentation workflows, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a pinned third-party npm CLI at use time to fetch public market data. <br>
Mitigation: Install only when this execution model is acceptable; in sensitive or production environments, review or sandbox westock-data-clawhub@1.0.4 and verify package integrity before use. <br>
Risk: Market data may be delayed or incomplete for decision-making contexts. <br>
Mitigation: Treat outputs as objective data retrieval, label currencies and units clearly, and verify critical values against official exchange or issuer sources before relying on them. <br>


## Reference(s): <br>
- [WeStock Data usage guide](references/ai_usage_guide.md) <br>
- [WeStock Data scenario guide](references/scenarios-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/westock-skills/westockdata) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/westock-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and concise text, with shell command examples; command failures may return JSON error objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a pinned npm CLI package at execution time and supports batch queries for most data commands except documented single-query commands such as search and minute.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
