## Description:

Pay-per-call GPU rental and AI inference via the Spraay x402 gateway, with prepaid compute-futures for discounted repeated jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they explicitly want to route GPU jobs, model inference, or prepaid compute-credit workflows through Spraay's paid x402 gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid calls and compute-futures deposits can spend or lock real USDC from a funded wallet.

Mitigation: Use a dedicated wallet with limited funds, check free estimates before paid calls, and require explicit confirmation before deposits or other paid operations.

Risk: Autonomous agents could trigger unwanted spending if the skill is activated too broadly.

Mitigation: Use the skill only for explicit Spraay or x402 compute requests and require human approval before paid actions.

## Reference(s):

- [Spraay x402 Gateway](https://gateway.spraay.app)
- [Spraay x402 Discovery Catalog](https://gateway.spraay.app/.well-known/x402.json)
- [ClawHub Skill Page](https://clawhub.ai/plagtech/skills/spraay-compute)
- [Publisher Profile](https://clawhub.ai/user/plagtech)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with HTTP endpoint examples and shell-oriented requirements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead an agent to make paid x402 requests that spend real USDC when the user confirms paid operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
