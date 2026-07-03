## Description: <br>
Volume profile analysis detecting accumulation or distribution patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to request real-time APEX Runner volume-profile signals for confirming breakouts, identifying accumulation or distribution, and informing momentum entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an EVM wallet private key for automatically paid x402 requests without clear per-call consent or spending limits. <br>
Mitigation: Use a dedicated low-balance wallet and only fund it with the amount you are willing to spend on calls. <br>
Risk: Each invocation may authorize a paid request. <br>
Mitigation: Review expected pricing before use and monitor wallet activity while the skill is enabled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/volume-analysis) <br>
- [APEX Runner Volume Analysis](https://apexrunner.ai/signals/volume-analysis) <br>
- [APEX Runner Pricing Tiers](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, JSON, Guidance] <br>
**Output Format:** [JSON response with signal fields and concise agent-facing analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402-authorized paid requests; each invocation may spend wallet funds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
