## Description:

Solana 链上智能分析与机会检测工具，用于分析 Solana 生态项目、检测新兴机会、追踪 Meme 币趋势、监控链上数据并提供投资决策参考.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Solana ecosystem health, evaluate new tokens, monitor launchpad activity, and produce risk-aware market intelligence for crypto research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an embedded payment-service API key.

Mitigation: Rotate the exposed key before installation and move payment credentials to environment-managed secrets.

Risk: The release evidence reports that wallet addresses can be sent to an external payment service without clear in-skill disclosure.

Mitigation: Document what wallet data is transmitted, obtain user approval before payment verification, and avoid sending wallet addresses unless required.

Risk: The skill provides crypto market and token opportunity guidance that may be incorrect, stale, or unsuitable for a user's circumstances.

Mitigation: Treat outputs as research support only, verify market data against authoritative sources, and avoid relying on the skill as financial advice.

## Reference(s):

- [Solana Intelligence Skill Page](https://clawhub.ai/shenmeng/skills/shenmeng-solana-intelligence)
- [Solana 链上分析脚本参考](references/api-reference.md)
- [Solana 生态核心项目参考](references/ecosystem.md)
- [Pump.fun 与新币发射分析指南](references/launchpad-guide.md)
- [CoinGecko Solana Ecosystem Markets API](https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=solana-ecosystem&order=market_cap_desc&per_page=100&page=1)
- [DefiLlama Solana Chain API](https://api.llama.fi/chain/Solana)
- [Solscan](https://solscan.io)
- [Solana Explorer](https://explorer.solana.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, Python code examples, shell commands, and JSON analysis files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external market-data and payment services when scripts are executed.]

## Skill Version(s):

1.0.0 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
