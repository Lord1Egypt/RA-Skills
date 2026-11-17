## Description:

土狗气象台 helps OpenClaw agents read public Web2 trending feeds from Tugou and extend relevant topics with public Binance Web3 crypto-market lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crime1000x](https://clawhub.ai/user/crime1000x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and OpenClaw agents use this skill to monitor public Chinese Web2 trends, identify meme or token-mapping candidates, and run read-only public Binance Web3 checks when a topic, token, contract, or wallet signal justifies follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public web requests may disclose queried wallet addresses, contract addresses, keywords, or research targets to Tugou and Binance Web3.

Mitigation: Submit only public addresses, contracts, and topics unless external querying is acceptable for the investigation.

Risk: Trend, market, audit, and smart-money results can be mistaken for financial advice.

Mitigation: Treat outputs as research signals, label uncertainty clearly, and avoid presenting results as investment recommendations.

Risk: Chinese trend-to-token mappings can be ambiguous when there is no confirmed contract address, liquidity signal, or sustained market activity.

Mitigation: Report mapping confidence and avoid strong conclusions unless the evidence supports an explicit token, contract, or address match.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crime1000x/skills/tugou-monitor)
- [Tugou public endpoint](https://tugoumeme.fun)
- [Binance Web3 public endpoint](https://web3.binance.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with curl command examples and structured research sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public web requests; no trading, posting, private-key, or destructive actions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
