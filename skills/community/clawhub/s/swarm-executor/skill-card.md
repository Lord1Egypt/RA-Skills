## Description:

Coordinate multi-agent swarm execution with a lightweight Pub/Sub protocol, standardized SwarmCommand messages, token-budget control, agent status tracking, negotiation, fallback, and completion gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xb19960921](https://clawhub.ai/user/xb19960921)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, validate, and operate multi-agent workflows with explicit ownership, state, token budgets, dependencies, fallback behavior, and completion gates. It is suited to agent orchestration tasks where parallel work improves throughput or review quality and where coordination risk must be controlled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Compose deployment can expose coordination and monitoring services with weak defaults.

Mitigation: Require non-empty Redis and Grafana secrets, bind services to loopback or an internal network, remove node-exporter unless host metrics are needed, and review the deployment before use.

Risk: Redis connectivity alone is not sufficient authorization to publish agent commands.

Mitigation: Validate command source, target role, budget, deadline, dependencies, and completion gate before publishing or accepting commands.

Risk: Swarm coordination can amplify mistakes when actions are destructive, public, costly, irreversible, or ambiguous.

Mitigation: Require human confirmation for high-risk actions and keep one accountable task owner plus an explicit fallback owner for each task.

Risk: Unpinned Python packages and container images can change behavior over time.

Mitigation: Pin Python dependencies and container image tags before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xb19960921/skills/swarm-executor)
- [SKILL.md](artifact/SKILL.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)
- [Swarm command schema](artifact/schemas/swarm_command.json)
- [Agent status schema](artifact/schemas/agent_status.json)
- [Compose deployment](artifact/docker-compose.yml)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command tables, JSON command examples, and optional Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize explicit task ownership, budgets, dependencies, fallback owners, and verification criteria.]

## Skill Version(s):

1.1.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG.md, coordinator package)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
