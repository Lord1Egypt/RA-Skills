## Description: <br>
Confirms whether the current trend has sufficient momentum to trade. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to query a paid APEX Runner signal before entering trend-following trades, filtering breakouts, or applying a final confirmation gate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a raw EVM private key for automatic x402-paid requests, so each invocation can spend USDC from the configured wallet. <br>
Mitigation: Use a dedicated low-balance wallet on Base mainnet and fund it only with amounts you are prepared to spend. <br>
Risk: The private key is supplied through EVM_PRIVATE_KEY and could expose wallet funds if leaked to logs, prompts, or shared environments. <br>
Mitigation: Store the key in a secret manager or isolated runtime environment, avoid echoing it in commands or logs, and rotate the wallet if exposure is suspected. <br>
Risk: The endpoint provides trading-signal guidance that may be incorrect or unsuitable for a user's strategy. <br>
Mitigation: Treat responses as one confirmation input, validate them against independent risk controls, and avoid autonomous trade execution without human-approved limits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/trend-confirmed) <br>
- [APEX Runner Trend Confirmed Signal](https://apexrunner.ai/signals/trend-confirmed) <br>
- [APEX Runner Pricing Check](https://apexrunner.ai/signals/my-pricing) <br>
- [Momentum Status Related Signal](https://apexrunner.ai/signals/momentum-status) <br>
- [Regime Related Signal](https://apexrunner.ai/signals/regime) <br>
- [APEX Composite Related Signal](https://apexrunner.ai/signals/apex-composite) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with Python and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402-authenticated paid requests; endpoint responses include confirmation, direction, and strength fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
