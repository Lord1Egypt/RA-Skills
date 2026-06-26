## Description: <br>
Real-time cryptocurrency price lookup from Upbit (Korean KRW exchange). Use when user asks for Korean crypto prices, Upbit prices, domestic cryptocurrency rates, or market ticker in Korean won (KRW). Supports all coins listed on Upbit exchange. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lkjsays](https://clawhub.ai/user/lkjsays) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to fetch public Upbit KRW-market cryptocurrency ticker data and format current price, daily movement, volume, and 52-week range details for user-facing answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public network requests to Upbit for cryptocurrency market data. <br>
Mitigation: Install only when public Upbit market-data lookups are acceptable for the agent's operating environment. <br>
Risk: Cryptocurrency market prices can change quickly and may be misread as investment advice. <br>
Mitigation: Present returned prices as informational market data and avoid treating them as financial advice. <br>
Risk: Unsupported or invalid market codes return an empty ticker response. <br>
Mitigation: Tell the user the coin is not available on Upbit or ask them to verify the KRW market code. <br>


## Reference(s): <br>
- [ClawHub Upbit Skill Page](https://clawhub.ai/lkjsays/upbit) <br>
- [Upbit Public Ticker API](https://api.upbit.com/v1/ticker?markets=KRW-BTC) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and formatted market data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Upbit ticker responses and does not require account credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
