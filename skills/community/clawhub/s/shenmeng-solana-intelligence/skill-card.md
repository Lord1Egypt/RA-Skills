## Description: <br>
Solana 链上智能分析与机会检测工具。用于分析 Solana 生态项目、检测新兴机会、追踪 Meme币趋势、监控链上数据和提供投资建议。当用户需要分析 Solana 生态、发现新项目、追踪链上机会、获取 Solana 市场情报或进行链上数据分析时触发此 Skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and crypto analysts use this skill to review Solana ecosystem health, evaluate new tokens and launchpad activity, monitor market and on-chain signals, and frame speculative research with explicit risk warnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a paid verification flow that may send wallet identifiers to SkillPay. <br>
Mitigation: Install only when that data sharing is acceptable, and avoid providing wallet addresses unless payment verification is required and approved. <br>
Risk: The artifact exposes a payment API key and uses an external verification service. <br>
Mitigation: Review and rotate payment credentials before deployment, and restrict execution of payment code to trusted environments. <br>
Risk: Token, launchpad, and market recommendations are speculative and may be misleading or financially harmful. <br>
Mitigation: Treat outputs as research support, verify claims against independent data sources, and avoid presenting analysis as financial advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shenmeng/shenmeng-solana-intelligence) <br>
- [Solana 链上分析脚本参考](references/api-reference.md) <br>
- [Solana 生态核心项目参考](references/ecosystem.md) <br>
- [Pump.fun 与新币发射分析指南](references/launchpad-guide.md) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=solana-ecosystem&order=market_cap_desc&per_page=100&page=1) <br>
- [DefiLlama Solana Data](https://defillama.com/chain/Solana) <br>
- [Solscan](https://solscan.io) <br>
- [Solana Explorer](https://explorer.solana.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, Python script references, and structured analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use external Solana, market-data, social-signal, and SkillPay verification services when the agent follows the artifact guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
