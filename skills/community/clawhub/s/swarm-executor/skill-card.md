## Description: <br>
Coordinate multi-agent swarm execution with a lightweight Pub/Sub protocol, standardized SwarmCommand messages, token-budget control, agent status tracking, negotiation, fallback, and completion gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xb19960921](https://clawhub.ai/user/xb19960921) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, validate, and operate multi-agent workflows with explicit task ownership, command schemas, token budgets, fallback rules, and completion gates. It is most useful when parallel agents need coordination without losing control of cost, state, or verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The compose stack exposes Redis, Grafana, Prometheus, and node-exporter services and includes default or environment-derived passwords. <br>
Mitigation: Review the compose stack before use, set explicit Redis and Grafana passwords, restrict exposed ports, and pin container images before deployment. <br>
Risk: Untrusted agents could misuse privileged IDs or bypass intended token-budget controls. <br>
Mitigation: Configure explicit maximum token limits and prevent untrusted agents from selecting privileged IDs such as 001. <br>
Risk: Treating the skill as a hardened production control plane could overstate its security posture. <br>
Mitigation: Use it as a coordination library unless additional authentication, network isolation, monitoring, and operational hardening are added. <br>
Risk: Swarm coordination can amplify mistakes for destructive, public, costly, irreversible, or ambiguous actions. <br>
Mitigation: Require human confirmation for high-risk actions and keep owner, budget, dependency, fallback, and done criteria explicit. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xb19960921/swarm-executor) <br>
- [Skill source](artifact/SKILL.md) <br>
- [Release changelog](artifact/CHANGELOG.md) <br>
- [Swarm command schema](artifact/schemas/swarm_command.json) <br>
- [Agent status schema](artifact/schemas/agent_status.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command examples, shell commands, and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include swarm plans, command tables, coordination flows, budget and downgrade policy, fallback rules, and verification criteria.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
