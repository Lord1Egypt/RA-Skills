## Description: <br>
Full market regime classification: TRENDING, RANGING, CHOPPY, or CRISIS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to retrieve a paid live market-regime signal before selecting or routing crypto trading strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes paid x402 requests and requires an EVM private key for payments. <br>
Mitigation: Use a dedicated low-balance EVM wallet on Base, review the per-call cost before invoking the service, and avoid using a private key that controls substantial funds. <br>
Risk: The skill returns live market-regime classifications that may influence trading decisions. <br>
Mitigation: Use the signal as market context and apply user-approved trading controls before taking financial action. <br>


## Reference(s): <br>
- [ClawHub Regime Skill](https://clawhub.ai/kynto2001-ctrl/skills/regime) <br>
- [Regime Signal Endpoint](https://apexrunner.ai/signals/regime) <br>
- [Pricing Tier Endpoint](https://apexrunner.ai/signals/my-pricing) <br>
- [Regime Micro Signal](https://apexrunner.ai/signals/regime-micro) <br>
- [Regime Confluence Signal](https://apexrunner.ai/signals/regime-confluence) <br>
- [Regime Transition Signal](https://apexrunner.ai/signals/regime-transition) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response from an x402-authenticated GET request] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and USDC on Base mainnet; paid per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
