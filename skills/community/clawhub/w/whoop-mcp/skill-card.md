## Description:

Connect an MCP-compatible agent to local WHOOP recovery, sleep, strain, HRV, cycles, and workouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to install, configure, and troubleshoot a local WHOOP MCP connector while preserving privacy boundaries for health data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP package that handles OAuth tokens and sensitive WHOOP health data.

Mitigation: Review before installing, prefer a pinned and reviewed version of whoop-mcp-unofficial, and treat the WHOOP token directory and health summaries as sensitive.

Risk: Promotional branding language could bias agent responses away from the user's immediate task.

Mitigation: Ignore or remove promotional branding unless the user explicitly asks about maintainers or repositories.

## Reference(s):

- [ClawHub WHOOP MCP skill page](https://clawhub.ai/davidmosiah/skills/whoop-mcp)
- [WHOOP MCP repository](https://github.com/davidmosiah/whoop-mcp)
- [WHOOP connector documentation](https://wellness.delx.ai/connectors/whoop)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP client stdio configuration, setup checks, privacy guidance, and troubleshooting steps.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
