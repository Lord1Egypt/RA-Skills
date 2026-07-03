## Description: <br>
Detects imminent regime transitions before they fully materialise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and trading-system developers use this skill to request a paid, wallet-authenticated signal for anticipating crypto market regime shifts and reducing exposure ahead of uncertainty. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses EVM_PRIVATE_KEY for wallet-based x402 payments, and each invocation may spend USDC on Base mainnet. <br>
Mitigation: Use a dedicated low-balance wallet, configure external spending limits and monitoring, and avoid recurring or autonomous use without separate payment controls. <br>
Risk: The security verdict is suspicious because the skill does not provide built-in spending controls or explicit per-call user consent. <br>
Mitigation: Require operator review or policy gating before enabling the skill, and inspect payment behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/regime-transition) <br>
- [Regime Transition signal](https://apexrunner.ai/signals/regime-transition) <br>
- [Pricing lookup](https://apexrunner.ai/signals/my-pricing) <br>
- [Regime signal](https://apexrunner.ai/signals/regime) <br>
- [Regime Confluence signal](https://apexrunner.ai/signals/regime-confluence) <br>
- [Regime Transition Probability signal](https://apexrunner.ai/signals/regime-transition-probability) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with a Python example and JSON response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and may spend USDC per invocation on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
