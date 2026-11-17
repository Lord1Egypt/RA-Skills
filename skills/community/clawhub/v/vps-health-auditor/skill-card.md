## Description:

Runs VPS and Linux server health diagnostics for CPU, memory, disk, network, services, uptime, and logs, then supports Ollama-powered reporting with recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gblockchainnetwork](https://clawhub.ai/user/gblockchainnetwork)

### License/Terms of Use:


## Use Case:

Developers and infrastructure operators use this skill to audit VPS or Linux server health and produce a concise report of operational issues and recommended follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages root SSH access for infrastructure auditing.

Mitigation: Use a dedicated low-privilege audit account and dedicated SSH key with only the permissions required for health checks.

Risk: The bundled SSH script can bypass host-key verification and mishandle user-supplied host, user, or key values.

Mitigation: Keep normal SSH host-key verification enabled, pass only trusted connection values, and harden the script with validation and shell quoting before use on real infrastructure.

Risk: Health reports may contain sensitive infrastructure details from service status, network, disk, or log output.

Mitigation: Review and redact generated reports before sharing them outside the operational team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gblockchainnetwork/skills/vps-health-auditor)
- [Publisher profile](https://clawhub.ai/user/gblockchainnetwork)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and diagnostic summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include VPS health findings, service status, log observations, and Ollama-generated recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
