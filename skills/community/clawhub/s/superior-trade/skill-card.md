## Description: <br>
Deprecated Superior Trade skill that redirects users to the maintained @superior-ai/superiortrade release while documenting API-key based backtesting and live deployment workflows for Superior Trade. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kan2k](https://clawhub.ai/user/kan2k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this deprecated skill to understand the former Superior Trade API workflow, create backtests, draft trading strategy configuration and code, and manage deployments. Because deployments can trade real funds, users should prefer the maintained successor package unless they specifically need this deprecated version. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is deprecated and points users to a maintained successor, but the artifact still documents workflows that can create live trading deployments. <br>
Mitigation: Prefer the maintained successor package unless this deprecated version is specifically required; review the release purpose before installing. <br>
Risk: The SUPERIOR_TRADE_API_KEY can create and manage backtests and deployments, including deployments that trade real funds. <br>
Mitigation: Store the key only in the agent environment or credential manager, never paste it into chat, and require explicit user confirmation before starting any live deployment. <br>
Risk: Incorrect wallet or balance assumptions can lead to misleading deployment guidance. <br>
Mitigation: Verify wallet status and balances with current API responses before reporting numbers or starting deployments, and check the platform-managed main wallet rather than the agent wallet. <br>
Risk: Generated strategy code or configuration can fail silently or place unintended trades if stake, pair, or exchange rules are wrong. <br>
Mitigation: Backtest first, validate pairs and minimum stake values, inspect logs for zero-trade or rate-limit behavior, and stop after repeated failures to simplify the strategy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kan2k/superior-trade) <br>
- [Maintained successor package](https://clawhub.ai/superior-ai/superiortrade) <br>
- [Superior Trade account portal](https://account.superior.trade) <br>
- [Superior Trade API docs](https://api.superior.trade/docs) <br>
- [Superior Trade OpenAPI spec](https://api.superior.trade/openapi.json) <br>
- [Hyperliquid public info endpoint](https://api.hyperliquid.xyz/info) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with JSON and Python code blocks plus concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce live-trading deployment instructions that require an environment API key and explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
1.5.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
