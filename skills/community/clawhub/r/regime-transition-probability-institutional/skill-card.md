## Description: <br>
Institutional regime transition model with confidence intervals <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to request paid APEX Runner regime transition probabilities for institutional regime risk management, probabilistic scenario modeling, and multi-week position planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an EVM private key for x402 payment authorization. <br>
Mitigation: Use a dedicated low-balance wallet, keep EVM_PRIVATE_KEY private, and avoid using a primary wallet. <br>
Risk: Each request may authorize a paid call to the APEX Runner signal. <br>
Mitigation: Review the published per-call pricing and monitor agent usage before enabling repeated calls. <br>


## Reference(s): <br>
- [APEX Runner regime transition probability institutional signal](https://apexrunner.ai/signals/regime-transition-probability-institutional) <br>
- [APEX Runner signal pricing tiers](https://apexrunner.ai/signals/my-pricing) <br>
- [Related regime transition probability signal](https://apexrunner.ai/signals/regime-transition-probability) <br>
- [Related regime confluence institutional signal](https://apexrunner.ai/signals/regime-confluence-institutional) <br>
- [Related cross-asset contagion institutional signal](https://apexrunner.ai/signals/cross-asset-contagion-institutional) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, JSON] <br>
**Output Format:** [Markdown instructions with a Python example and JSON response from an x402-authenticated HTTP GET] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and an EVM wallet with USDC on Base mainnet; requests may authorize a per-call x402 payment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
