## Description: <br>
Provides real-time momentum, whale sentiment, and regime confluence crypto trading signals from APEX Runner's live autonomous trading system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to request a paid, one-call crypto trading-signal bundle for multi-factor trading analysis. It combines momentum, whale sentiment, and regime confluence signals from APEX Runner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic x402 requests can spend USDC from the configured wallet. <br>
Mitigation: Use a dedicated low-balance Base wallet funded only with the USDC you are willing to spend. <br>
Risk: The skill requires access to an EVM private key for payment authorization. <br>
Mitigation: Avoid reusing a primary wallet private key and provide only an isolated wallet key through the required environment variable. <br>
Risk: Trading signals may be incorrect, delayed, or unsuitable for a user's trading strategy. <br>
Mitigation: Treat responses as decision support and review them before making trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/trading-intelligence-bundle) <br>
- [Trading Intelligence Bundle endpoint](https://apexrunner.ai/signals/trading-intelligence-bundle) <br>
- [Market Pulse Bundle](https://apexrunner.ai/signals/market-pulse-bundle) <br>
- [Risk Assessment Bundle](https://apexrunner.ai/signals/risk-assessment-bundle) <br>
- [APEX Composite](https://apexrunner.ai/signals/apex-composite) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, code, configuration, guidance] <br>
**Output Format:** [JSON response from an x402-authenticated GET request, with Markdown instructions and a Python example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402 payment authorization; each call can trigger an automatic paid request in USDC on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
