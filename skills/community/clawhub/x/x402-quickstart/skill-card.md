## Description:

Deploy x402 pay-per-call API endpoints in minutes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmyclanker](https://clawhub.ai/user/jimmyclanker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold x402-compatible Express API endpoints that charge AI agents USDC on Base for pay-per-call access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated scaffold should be treated as prototype payment infrastructure rather than production-ready payment enforcement.

Mitigation: Review generated files before installation or deployment, then add production authentication, rate limits, logging, and payment enforcement controls.

Risk: Payment replay or weak payment binding could allow access without a fresh, endpoint-specific payment.

Mitigation: Add proper invoice or nonce-based payment binding with persistent atomic replay protection before public use.

Risk: Public tunnel exposure can make unfinished endpoints reachable on the internet.

Mitigation: Expose endpoints publicly only after validating project names, wallet configuration, access controls, and monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimmyclanker/skills/x402-quickstart)
- [Publisher profile](https://clawhub.ai/user/jimmyclanker)
- [Spraay Gateway](https://gateway.spraay.app)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, JavaScript, JSON, and environment variable snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a scaffolded Express project with x402 payment middleware when the included shell script is run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
