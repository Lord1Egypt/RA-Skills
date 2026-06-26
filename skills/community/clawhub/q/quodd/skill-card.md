## Description: <br>
Fetch real-time stock quotes via Quodd API. Get current prices, daily high/low, and after-hours data for US equities. Use when the user asks for stock prices, quotes, market data, or ticker information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khaney64](https://clawhub.ai/user/khaney64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve current US equity quote data from Quodd, including daily high, daily low, last trade price, and after-hours values for one or more ticker symbols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to Quodd account credentials and sends them to Quodd to obtain an API token. <br>
Mitigation: Use dedicated Quodd credentials where possible and avoid setting them in shared shells. <br>
Risk: The skill caches the Quodd token at ~/.openclaw/credentials/quodd-token.json for up to 20 hours. <br>
Mitigation: Remove ~/.openclaw/credentials/quodd-token.json to clear the cached token before expiry, especially after credential rotation or on shared systems. <br>


## Reference(s): <br>
- [Quodd Stock and ETF Data](https://www.quodd.com/stock-and-etf-data) <br>
- [Quodd on ClawHub](https://clawhub.ai/khaney64/quodd) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Text, JSON] <br>
**Output Format:** [Plain text table or JSON object containing quote fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and QUODD_USERNAME and QUODD_PASSWORD environment variables; caches a Quodd authentication token locally for 20 hours unless --no-cache is used.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
