## Description:

Routes user intents to available Reson8-Labs skills, MCP tools, integrations, and marketplace packaging paths, including multi-step skill chains with WAVE transition checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toolate28](https://clawhub.ai/user/toolate28)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and external agents use this skill to inventory available capabilities, select or compose skill chains, and identify packaging paths for integrations and marketplace releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad orchestration requests can route into cloud provisioning, calendar access, public posting, deployment, package publishing, or persistent file and memory updates.

Mitigation: Require explicit confirmation before every external write, public post, deployment, package publish, credentialed action, or persistent state change.

Risk: Suggested third-party installs or marketplace packaging steps can introduce unreviewed dependencies or external services.

Mitigation: Pin, sandbox, and review third-party installs and generated packaging instructions before use.

Risk: Multi-step skill chains can carry incorrect assumptions from one step into later actions.

Mitigation: Review proposed chains and use transition checks as advisory gates before executing sensitive or irreversible steps.

## Reference(s):

- [Activation Map](references/activation-map.md)
- [Composition Patterns](references/composition-patterns.md)
- [Marketplace Bridges](references/marketplace-bridges.md)
- [ClawHub Skill Listing](https://clawhub.ai/toolate28/skills/reson8-activator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with ordered activation plans, capability inventories, and command or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose chained actions that require user confirmation before external writes, credentialed operations, deployments, publishing, or persistent state changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
