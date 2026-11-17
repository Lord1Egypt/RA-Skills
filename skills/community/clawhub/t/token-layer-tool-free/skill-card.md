## Description: <br>
Queries cross-chain token data for mainstream networks, including contract addresses, prices, and liquidity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External crypto users and developers use this skill to look up token addresses, pricing, liquidity, and chain-specific token details across Ethereum, BSC, Polygon, Arbitrum, and Optimism. Outputs are intended for token research and reporting support, not financial advice or real-time monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command execution and file-writing capability for token data lookup workflows. <br>
Mitigation: Review commands before execution and run the skill in a workspace where local cache or export files are acceptable. <br>
Risk: The skill may use blockchain API keys and RPC endpoints from local environment variables. <br>
Mitigation: Store keys in local environment variables only, use least-privileged API keys where available, and avoid pasting secrets into prompts or output. <br>
Risk: Token prices, liquidity, and contract data may be delayed or inaccurate and can affect investment decisions. <br>
Mitigation: Verify contract addresses and market data against authoritative sources before acting; treat results as research support, not financial advice. <br>
Risk: Server security evidence marks the release as suspicious because broad activation language and unclear export behavior accompany command and write permissions. <br>
Mitigation: Install only after reviewing the skill source and scanner guidance, and prefer constrained execution permissions when the agent platform supports them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/token-layer-tool-free) <br>
- [Etherscan API endpoint](https://api.etherscan.io) <br>
- [BSCScan API endpoint](https://api.bscscan.com) <br>
- [PolygonScan API endpoint](https://api.polygonscan.com) <br>
- [BSC public RPC endpoint](https://bsc-dataseed.binance.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured token-query responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include status codes, result data, logs, and local environment-variable setup guidance for optional API keys.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
