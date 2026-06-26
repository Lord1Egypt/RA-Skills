## Description: <br>
Solana Trading Api helps agents prepare Solana swaps, submit signed transactions through TradeRouter, inspect wallet holdings, and manage limit, trailing, TWAP, and combo orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[re-bruce-wayne](https://clawhub.ai/user/re-bruce-wayne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and trading agents use this skill to build Solana token trading workflows through the TradeRouter API, including swap construction, MEV-protected submission, wallet holdings checks, and persistent WebSocket order management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through real Solana trades using wallet signing authority. <br>
Mitigation: Use a dedicated low-balance wallet, keep dry-run mode enabled until tested, and require explicit confirmation for token, side, amount, slippage, expiry, and cancellation policy. <br>
Risk: Persistent WebSocket orders can remain active after placement. <br>
Mitigation: Track open order IDs, keep the WebSocket connected while orders are active, and check or cancel open orders after use. <br>
Risk: Private key handling is required for signing transactions and WebSocket challenge responses. <br>
Mitigation: Never expose a main wallet private key; sign only in a secure client environment and avoid logging secrets or signed payload material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/re-bruce-wayne/trade-router) <br>
- [TradeRouter website](https://traderouter.ai) <br>
- [TradeRouter API base](https://api.traderouter.ai) <br>
- [TradeRouter security endpoint](https://api.traderouter.ai/security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes trading workflow guidance that should be reviewed before live execution.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
