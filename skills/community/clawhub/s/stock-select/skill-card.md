## Description: <br>
Stock Select helps agents query stock market data, run natural-language stock screens, monitor Level2 and call-auction signals, manage brokerage accounts, and prepare or submit assisted trade orders through Stockboot APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghl-cn](https://clawhub.ai/user/wanghl-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search for stocks with natural-language criteria, retrieve market and account data, and assist with order entry against supported brokerage accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can receive brokerage login or session data and account identifiers. <br>
Mitigation: Install only from a trusted publisher, avoid sharing tokens in logs or chats, and use short-lived session handling without persistent token storage. <br>
Risk: The skill can assist with live buy or sell orders through an external API. <br>
Mitigation: Require explicit per-order confirmation and verify account, symbol, side, price, quantity, and order type before submitting any trade. <br>
Risk: The skill depends on an external Stockboot API for market, account, and trading actions. <br>
Mitigation: Review the configured API endpoint, start with read-only market features, and use self-hosting only when the deployment and credential handling are trusted. <br>


## Reference(s): <br>
- [Stockbot website](https://stockbot.me) <br>
- [Stockboot API endpoint](https://api.stockbot.me) <br>
- [ClawHub skill listing](https://clawhub.ai/wanghl-cn/stock-select) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with API request examples, shell commands, and structured guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authentication tokens, account identifiers, stock symbols, screening criteria, and trade order details supplied by the user.] <br>

## Skill Version(s): <br>
2.0.2 (source: server evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
