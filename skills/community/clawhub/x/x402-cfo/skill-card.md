## Description:

Financial brain for x402 payments: budget enforcement, cost policies, spend analytics, anomaly detection, and audit trail for autonomous agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upn-130guthub](https://clawhub.ai/user/upn-130guthub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and autonomous-agent operators use this skill to route x402 paid API calls through AgentCFO so budgets, per-request policies, spend analytics, anomaly alerts, and audit logs are applied before wallet payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates wallet-based payment authority and the security summary flags broad defaults.

Mitigation: Restrict the wallet or session key to small limits and approved recipients, add an explicit destination allowlist, and require confirmation before the first payment to any new endpoint.

Risk: The setup command installs x402-cfo without a pinned version.

Mitigation: Use a pinned and audited x402-cfo version, preferably installed with npm ci and a committed lockfile.

Risk: The local ledger records payment audit details.

Mitigation: Decide before use whether ./x402-cfo-ledger.json is acceptable in the project and handle it according to the project's data retention and privacy expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upn-130guthub/skills/x402-cfo)
- [Publisher profile](https://clawhub.ai/user/upn-130guthub)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes budget policy guidance, spend summary and audit guidance, event-handling guidance, and environment variable configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and release changelog mention 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
