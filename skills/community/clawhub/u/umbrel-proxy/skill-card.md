## Description:

Efficiently manage and interact with Umbrel proxy services for Docker containers by discovering running services, mapping internal Docker IPs to accessible host ports, and updating OpenClaw config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmoranxyz](https://clawhub.ai/user/gmoranxyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing OpenClaw with Umbrel use this skill to discover local Umbrel proxy endpoints, test service connectivity, and update plugin base URLs after service or container changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The config-updating workflow can turn service mapping data into OpenClaw configuration commands.

Mitigation: Review mapping files before use, prefer dry-run mode where available, and back up OpenClaw configuration before applying updates.

Risk: Running the sync scripts unattended could apply incorrect service URLs or stale mappings.

Mitigation: Run the scripts interactively until command construction and write controls are reviewed, then verify connectivity and plugin behavior before restarting the gateway.

Risk: Elevated privileges can increase the impact of unintended configuration changes.

Mitigation: Avoid running the workflow as root unless required by the local Docker and OpenClaw setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gmoranxyz/skills/umbrel-proxy)
- [Publisher profile](https://clawhub.ai/user/gmoranxyz)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, local URLs, status summaries, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may generate or update local JSON mapping and connectivity result files when run.]

## Skill Version(s):

1.0.3 (source: server release evidence, package.json, and CHANGELOG; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
