## Description: <br>
Predicts expected slippage for a given order size and market condition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill before placing large crypto orders to estimate expected slippage, compare venues, and understand realistic execution costs from APEX Runner's live trading signal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: x402-authenticated requests can automatically spend wallet funds per call. <br>
Mitigation: Use a dedicated low-balance wallet and configure X402_POLICY_PATH with per-transaction caps, daily caps, and recipient allowlists before use. <br>
Risk: The skill is a paid API gateway, and spending limits are optional rather than guaranteed. <br>
Mitigation: Review wallet balances, policy settings, and expected call volume before broad or automated use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/slippage-forecast) <br>
- [APEX Runner slippage forecast signal](https://apexrunner.ai/signals/slippage-forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API response examples and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402-authenticated paid requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
