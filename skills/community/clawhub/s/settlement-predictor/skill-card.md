## Description: <br>
Real-time on-chain settlement predictor for Ethereum, Bitcoin, Arbitrum, Optimism, Base, and Polygon with gas tiers, mempool analysis, sandwich-risk detection, transaction tracking, and fee trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ethanwuqi-lang](https://clawhub.ai/user/ethanwuqi-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, Web3 operators, and blockchain users use this skill to estimate transaction settlement timing, monitor gas and fee trends, inspect pending-pool risk, and track EVM or Bitcoin transactions before and after submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried blockchain identifiers may be sent to public RPC, explorer, mempool.space, CoinGecko, Tenderly, or Etherscan services. <br>
Mitigation: Use the skill only when this disclosure is acceptable for the addresses, pools, tokens, and transaction hashes being queried. <br>
Risk: Optional API keys expand the services contacted by the skill. <br>
Mitigation: Set ETHERSCAN_API_KEY or TENDERLY_API_KEY only for the features you need, and do not provide private keys or seed phrases. <br>
Risk: Fee history is retained locally for trend analysis. <br>
Mitigation: Delete ~/.cache/settlement-predictor when local fee-history retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ethanwuqi-lang/settlement-predictor) <br>
- [Etherscan API key setup](https://etherscan.io/myapikey) <br>
- [Tenderly dashboard](https://dashboard.tenderly.co/) <br>
- [mempool.space](https://mempool.space) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, JSON, or table output with command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include live blockchain fee estimates, transaction status, risk indicators, and locally cached fee-history trends.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
