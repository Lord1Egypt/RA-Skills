## Description:

Guides agents through reviewing x402 payment terms and Base recipient risks before a user-authorized purchase or wallet interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xavierleterrible-hub](https://clawhub.ai/user/xavierleterrible-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect an unfamiliar x402 endpoint or Base address before a user-authorized transaction, check payment terms against an approved budget, and interpret preflight warnings without treating them as a safety guarantee.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs or Base addresses are sent to SignalLayer for analysis.

Mitigation: Submit only targets you are comfortable sharing with SignalLayer.

Risk: The optional wallet example can spend real USDC, and its CLI version is unpinned.

Mitigation: Verify the package and live recipient, Base USDC asset and 0.01 USDC cap; require explicit approval before any payment.

Risk: Preflight results may be incomplete or mistaken and do not establish recipient safety.

Mitigation: Review evidence, warnings and freshness; require separate authorization for any later payment or wallet interaction.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xavierleterrible-hub/skills/signallayer-preflight)
- [SignalLayer](https://signallayer.floot.app)
- [SignalLayer API specification](https://signallayer.floot.app/openapi.json)
- [SignalLayer MCP endpoint](https://signallayer.floot.app/_api/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Analysis]

**Output Format:** [Markdown guidance with optional structured JSON findings from the service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid findings include a decision, evidence, warnings, freshness and next actions; the skill does not sign payments.]

## Skill Version(s):

0.1.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
