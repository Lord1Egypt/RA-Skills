## Description: <br>
Valiron intercepts and authorizes outgoing machine-to-machine payments using @valiron/sdk trust decisions before payment execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vatsashah45](https://clawhub.ai/user/vatsashah45) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Valiron to add a trust gate before outgoing agent payment flows, including x402-style purchases, wallet spend guards, policy engines, and auditable allow, deny, throttle, or fallback decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A compromised or unexpected @valiron/sdk package could affect payment authorization behavior. <br>
Mitigation: Review @valiron/sdk provenance before installation and pin approved dependency versions in the host application. <br>
Risk: Payment credentials or API keys could be exposed through configuration or logs. <br>
Mitigation: Store VALIRON_API_KEY in a secrets manager, avoid hardcoded credentials, and redact secrets from audit events. <br>
Risk: Incorrect route policy or spend limits could allow payments outside the intended risk posture. <br>
Mitigation: Validate the decision policy, test representative routes before deployment, and use fail-closed defaults for production or high-value flows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vatsashah45/valiron-trust-layer) <br>
- [Runtime Requirements](references/runtime-requirements.md) <br>
- [Decision Policy](references/decision-policy.md) <br>
- [Spend Controls](references/spend-controls.md) <br>
- [Fallback Modes](references/fallback-modes.md) <br>
- [Audit Event Schema](references/audit-events.md) <br>
- [Error Handling](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with TypeScript and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes payment policy validation, spend controls, fallback behavior, and audit logging guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
