## Description: <br>
Trade security tokens on the X platform — check balances, place orders, view market data, and review trade history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seineruo](https://clawhub.ai/user/seineruo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage X platform security-token accounts, inspect balances and market data, place or cancel orders, and review trade history through authenticated API requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private financial account, balance, position, order, and transaction data. <br>
Mitigation: Use a dedicated least-privilege API key, avoid shared-screen disclosure, and require explicit user confirmation before showing sensitive history or account details. <br>
Risk: The skill can guide live order placement and cancellation for security tokens. <br>
Mitigation: Repeat symbol, side, order type, quantity, and price before action; proceed only after explicit confirmation and warn on large orders. <br>
Risk: Exposure of X_TRADING_API_KEY would allow unauthorized API access within the key's permissions. <br>
Mitigation: Store the key only in the environment, never paste it into chat, and do not log or repeat it in responses. <br>
Risk: Broad activation triggers may cause trading modules to load for ambiguous user requests. <br>
Mitigation: Restrict execution to clear X platform trading intents and ask follow-up questions whenever symbol, amount, order type, or date range is ambiguous. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/seineruo/x-trade) <br>
- [X Trading API access](https://xtrading.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown with API request examples, tables, and concise user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X_TRADING_API_KEY for authenticated account, order, market data, and history requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
