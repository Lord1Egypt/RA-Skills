## Description:

Audit an agent/API origin for well-known discovery, x402 pricing, OpenAPI/MCP readiness, and install blockers before an agent integrates it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastiancoombs](https://clawhub.ai/user/sebastiancoombs)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, OpenClaw users, and autonomous agents use this skill to assess whether an agent or API origin is ready to integrate, trust, pay, debug, or reject before relying on its discovery and x402 surfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can overwrite or delete directories outside the intended OpenClaw skills folder if given a crafted install name.

Mitigation: Review before installing, do not use an untrusted --name value, and avoid --force until destination containment is validated.

Risk: Paid x402 backend calls can incur cost when an agent follows the workflow.

Mitigation: Keep payment approval in wallet policy and verify the x402 price, network, and payTo before any paid call.

Risk: External web and API content gathered during an audit can be incomplete, contradictory, or adversarial.

Mitigation: Treat external content as evidence rather than instructions, report uncertainty, and avoid treating a missing or failed upstream response as proof of safety.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sebastiancoombs/skills/wellknown-audit-corpus-skill)
- [Production audit backend](https://wellknown-audit-corpus.mtree.workers.dev)
- [OpenClaw skill capabilities schema](https://openclaw.ai/schemas/skill-capabilities/v0.1)
- [Package security notes](artifact/PACKAGE_SECURITY.md)
- [Package provenance notes](artifact/PACKAGE_PROVENANCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise Markdown report with verdict, evidence, cost, and next action; optional curl examples and JSON request bodies.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include missing discovery surfaces, x402 price and network details, setup friction, and uncertainty when upstream discovery fails.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact files report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
