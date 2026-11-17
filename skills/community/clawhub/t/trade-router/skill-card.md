## Description:

Solana swap execution, MEV-protected transaction submission, wallet scanning, and market-cap-based limit, trailing, TWAP, and combo order guidance via the TradeRouter API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[re-bruce-wayne](https://clawhub.ai/user/re-bruce-wayne)

### License/Terms of Use:


## Use Case:

External developers and trading agents use this skill to build Solana swaps, inspect wallet holdings, submit signed transactions, and manage market-cap-based orders through the TradeRouter API. The skill is intended for agents that can prepare API requests, sign transactions with a wallet key, and apply trading safety checks before live execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to sign and submit remote-built Solana transactions with a wallet key before transaction contents are independently checked.

Mitigation: Use only a dedicated, low-balance wallet, keep dry-run enabled during review, and require local transaction validation or human confirmation before live signing.

Risk: Live order flows require wallet signing authority for WebSocket challenge response and subsequent transaction execution.

Mitigation: Keep the wallet key scoped to this trading use case, avoid primary wallets, and enable live mode only after reviewing order parameters and safety limits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/re-bruce-wayne/skills/trade-router)
- [TradeRouter Website](https://traderouter.ai)
- [TradeRouter API](https://api.traderouter.ai)
- [TradeRouter WebSocket API](wss://api.traderouter.ai/ws)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Markdown with JSON examples, API payloads, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes trading workflow guidance, transaction signing steps, timeout guidance, WebSocket order flows, and dry-run/live-mode configuration notes.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
