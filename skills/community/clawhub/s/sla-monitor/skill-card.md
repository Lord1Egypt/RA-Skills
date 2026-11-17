## Description:

Set up SLA monitoring and uptime tracking for production AI agents and services, including monitoring configs, alert rules, and incident response playbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers, operators, and service teams use this skill to define uptime monitors, SLA tiers, alert escalation, incident response steps, error budgets, and status page content for production AI agents and automated services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The self-hosted monitoring example can expose a persistent Uptime Kuma service on port 3001 without access controls.

Mitigation: Bind the service to localhost or restrict access with firewall or security-group rules, and place any remote access behind authenticated TLS.

Risk: The Docker command uses an image tag and restart policy that may be difficult to govern in production.

Mitigation: Pin the Uptime Kuma image to a reviewed digest, and define restart, volume, update, and rollback procedures before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/sla-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SLA tier examples, alert configuration templates, incident response playbooks, an error budget calculator, and status page guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
