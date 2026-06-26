## Description: <br>
Analyze any TRON account's assets, token holdings, staking, voting, energy/bandwidth, and transaction patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greason](https://clawhub.ai/user/greason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to profile public TRON addresses, check balances and token holdings, review staking and voting status, and summarize account activity patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TRON wallet addresses and activity can be privacy-sensitive when linked to a person or organization. <br>
Mitigation: Treat addresses as sensitive context, avoid identity claims unless supplied by the user, and prefer a basic balance lookup when detailed profiling is unnecessary. <br>
Risk: Account classifications and DeFi participation summaries are interpretations of public on-chain activity and may be incomplete or misleading. <br>
Mitigation: Frame conclusions as observed public indicators, preserve uncertainty, and separate raw balances or transactions from inferred behavior. <br>


## Reference(s): <br>
- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown account profile with tables and concise narrative summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public wallet balances, token holdings, staking and voting details, resource usage, transaction-pattern summaries, and account classification.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
