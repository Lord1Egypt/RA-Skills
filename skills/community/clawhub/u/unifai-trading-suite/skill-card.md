## Description: <br>
AI-powered trading insights suite: prediction markets (Polymarket/Kalshi) and social sentiment signals powered by UnifAI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zbruceli](https://clawhub.ai/user/zbruceli) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to query and compare prediction-market data across Polymarket and Kalshi and to summarize crypto social sentiment signals for trading research. It supports analysis, guidance, and command generation rather than autonomous live trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad financial-tool access with weak scoping can expose an agent to unintended market, wallet, or trading actions. <br>
Mitigation: Use read-only or non-privileged API keys, avoid connecting wallets or live trading credentials, and audit or constrain available UnifAI tools before enabling generic chat or server paths. <br>
Risk: Prompts, conversation context, and tool results may be sent to external LLM, market-data, and social-signal providers. <br>
Mitigation: Do not provide sensitive account, wallet, portfolio, or personal data unless the relevant provider policies and deployment controls have been reviewed. <br>
Risk: Market probabilities, social sentiment, and news signals can be incomplete, delayed, or misleading for financial decisions. <br>
Mitigation: Treat outputs as research support, verify claims against primary market sources, and require human review before any financial action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zbruceli/unifai-trading-suite) <br>
- [Project homepage from skill metadata](https://github.com/zbruceli/trading) <br>
- [UnifAI SDK](https://github.com/unifai-network/unifai-sdk-py) <br>
- [LiteLLM documentation](https://docs.litellm.ai/) <br>
- [Kalshi API documentation](https://docs.kalshi.com) <br>
- [Polymarket documentation](https://docs.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands and structured market summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external LLM, market-data, and social-signal providers; requires API keys for some paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
