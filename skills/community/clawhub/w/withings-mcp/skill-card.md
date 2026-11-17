## Description:

Connect an MCP-compatible agent to local Withings body measures, sleep, activity, workouts, and heart records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to install, configure, troubleshoot, and safely operate Withings MCP with MCP-compatible clients while keeping OAuth tokens and health data private.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned npm package that handles Withings OAuth tokens and sensitive health data.

Mitigation: Pin a specific trusted version of withings-mcp-unofficial, verify the package source and publisher, and review the skill before installing.

Risk: OAuth tokens, local token files, or health data could be exposed in chat, logs, or agent output.

Mitigation: Avoid exposing token files or health data in chat, keep user consent explicit, and prefer status, manifest, doctor, privacy audit, or dry-run flows before live calls.

Risk: The MCP server may access sensitive local Withings data during agent use.

Mitigation: Run the MCP server under a dedicated low-privilege account or sandbox where practical.

## Reference(s):

- [Withings MCP repository](https://github.com/davidmosiah/withingsmcp)
- [Withings connector documentation](https://wellness.delx.ai/connectors/withings)
- [ClawHub skill page](https://clawhub.ai/davidmosiah/skills/withings-mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, usage, safety-boundary, and troubleshooting guidance for MCP-compatible agents.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
