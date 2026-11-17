## Description:

Inspect supported Base USDC/WETH swap eligibility or request a SafeRoute quote via x402. Payment needs the operator's approved client and budget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crystalsignal](https://clawhub.ai/user/crystalsignal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect whether a supported Base USDC/WETH swap meets SafeRoute's safety checks or to request an optional quote. Paid requests require the operator's existing payment client and an approved spending limit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid requests rely on the operator's existing payment client; the live service and external payment client were not verified.

Mitigation: Start with the unpaid inspection. For paid use, enforce the approved merchant, Base USDC, and a 0.001 USDC limit; quotes need a separate 0.01 USDC allowance. Keep wallet secrets in the local client.

Risk: A safety result is indicative and does not guarantee against loss or establish that a trade was executed.

Mitigation: Treat the result as limited evidence, validate any later action separately, and do not sign or broadcast a trade solely because of this check.

## Reference(s):

- [SafeRoute OpenAPI specification](https://api.usesaferoute.com/openapi.json)
- [SafeRoute developer guide](https://usesaferoute.com/developers)
- [SafeRoute first-call guide](https://usesaferoute.com/start)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON]

**Output Format:** [Markdown guidance and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Eligibility results are indicative; they do not guarantee an outcome or prove trade execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
