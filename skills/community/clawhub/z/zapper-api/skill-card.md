## Description: <br>
Query DeFi portfolios, token holdings, NFTs, transactions, and prices via Zapper API across 50+ chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zivhm](https://clawhub.ai/user/zivhm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and crypto operators use this skill to query wallet balances, DeFi positions, NFT collections, token prices, claimable rewards, and transaction history through Zapper's API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, labels, and portfolio or transaction-history queries are sent to Zapper and may also appear in local configuration or command output. <br>
Mitigation: Use a dedicated Zapper API key, keep ~/.config/zapper/addresses.json private, and avoid storing labels or addresses you do not want exposed. <br>
Risk: Results depend on Zapper API availability, tier access, rate limits, NFT floor-price estimates, and the documented 30-day transaction-history window. <br>
Mitigation: Verify important balances, prices, and transaction details against primary sources before relying on them, and avoid rapid repeated requests. <br>


## Reference(s): <br>
- [Zapper API Reference](references/API.md) <br>
- [Zapper API Documentation](https://build.zapper.xyz/docs/api/) <br>
- [Zapper Developers](https://zapper.xyz/developers) <br>
- [Zapper](https://zapper.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples; command output can be text summaries or raw JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a ZAPPER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
