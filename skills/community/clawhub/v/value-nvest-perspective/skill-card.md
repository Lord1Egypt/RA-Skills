## Description: <br>
Value Nvest Perspective helps agents evaluate US stock and long-call option setups through a quality-growth, patience-first investment framework that emphasizes current market data and bounded, conditional advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ting2tao](https://clawhub.ai/user/ting2tao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to discuss US tech stock, M7, AI infrastructure, and long-call allocation questions, including whether to buy, hold, rotate, or wait. It is market research support, not personalized financial advice or trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat market commentary as personalized financial advice or a trade recommendation. <br>
Mitigation: Use the skill as market research support only, and independently verify prices, option-chain data, risk tolerance, and suitability before trading. <br>
Risk: Market prices, macro data, and option conditions may be stale or unavailable during a session. <br>
Mitigation: Refresh market data through Longbridge or web search before forming a view, and ask the user for current prices, holdings, and time horizon when live data is unavailable. <br>
Risk: Optional market-data setup can connect the agent to an external Longbridge service. <br>
Mitigation: Only run the optional npx install or Claude Longbridge MCP setup when the user trusts the source and is comfortable connecting that market-data provider. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ting2tao/value-nvest-perspective) <br>
- [Research source map](artifact/references/research/01-source-map.md) <br>
- [Market lens](artifact/references/research/02-market-lens.md) <br>
- [Options playbook](artifact/references/research/03-options-playbook.md) <br>
- [Risk and positioning](artifact/references/research/04-risk-and-positioning.md) <br>
- [Boundaries and open questions](artifact/references/research/06-boundaries-and-open-questions.md) <br>
- [Captured Longbridge source links](artifact/references/sources/captured-links.md) <br>
- [ValueNvest Longbridge profile](https://longbridge.com/zh-CN/profiles/14581970/original) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text investment-analysis guidance with conditional recommendations and occasional inline commands for market-data setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should verify current market data when available, avoid exact option strike or expiration claims without user-provided chain data, and include invalidation conditions for investment views.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
