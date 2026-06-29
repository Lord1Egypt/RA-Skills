## Description: <br>
Provides real-time portfolio heat, liquidation pressure, and position exposure risk metrics from APEX Runner's live trading system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill before large position changes, for periodic risk monitoring, or when building crypto risk dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each use may trigger a paid x402 request to APEX Runner. <br>
Mitigation: Confirm the per-call cost before use and treat each invocation as a potential paid request. <br>
Risk: The skill uses an EVM wallet for payment authorization. <br>
Mitigation: Use a dedicated low-balance wallet rather than a primary wallet. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/risk-assessment-bundle) <br>
- [APEX Runner Risk Assessment Bundle](https://apexrunner.ai/signals/risk-assessment-bundle) <br>
- [APEX Runner Pricing Tier Check](https://apexrunner.ai/signals/my-pricing) <br>
- [APEX Runner Portfolio Heat Signal](https://apexrunner.ai/signals/portfolio-heat) <br>


## Skill Output: <br>
**Output Type(s):** [json, guidance] <br>
**Output Format:** [JSON response with concise usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an x402-authenticated GET request and requires an EVM wallet with USDC on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
