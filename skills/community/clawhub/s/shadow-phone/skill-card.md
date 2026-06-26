## Description: <br>
Get a disposable temp phone number and receive OTP codes to sign up on websites without using your real number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xShadowETH](https://clawhub.ai/user/0xShadowETH) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to obtain a disposable phone number, pay the provider through x402, receive an SMS/OTP code, and complete an authorized phone verification workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger automatic crypto payments for each disposable phone number purchase. <br>
Mitigation: Use a dedicated wallet with minimal funds and require manual approval before each payment. <br>
Risk: Disposable phone verification can be misused for account creation or verification flows without permission. <br>
Mitigation: Use only for workflows the user owns or has explicit permission to test, and require confirmation before entering an OTP. <br>
Risk: The agent may handle both wallet credentials and temporary SMS verification codes. <br>
Mitigation: Limit SHADOW_WALLET_KEY scope, avoid using sensitive accounts, and do not persist OTP values after the verification step. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xShadowETH/shadow-phone) <br>
- [Shadow API Endpoint](https://extraordinary-charisma-production.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHADOW_WALLET_KEY and may trigger per-number x402 payments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
