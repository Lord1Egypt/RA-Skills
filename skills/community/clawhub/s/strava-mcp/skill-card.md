## Description:

Connect an MCP-compatible agent to local Strava activities, streams, routes, athlete stats, gear, and clubs. Use when an AI agent needs setup, usage, safety boundaries, or troubleshooting for Strava MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and MCP-compatible agent users use this skill to install, configure, and safely operate Strava MCP for access to Strava activities, streams, routes, athlete stats, gear, and clubs. It helps agents provide setup guidance, usage prompts, privacy checks, and troubleshooting boundaries for Strava data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow runs a mutable, unpinned npm MCP package through npx.

Mitigation: Pin strava-mcp-unofficial to a reviewed exact version before deployment and review package changes before upgrading.

Risk: The MCP process may handle OAuth tokens, GPS data, activity data, and other private Strava information.

Mitigation: Limit the process's filesystem and environment access, avoid printing secrets or private payloads, and keep location-level data access opt-in.

Risk: Live provider calls or writes could expose data or exceed Strava API expectations without explicit user consent.

Mitigation: Prefer connection_status, manifest, doctor, privacy_audit, or dry-run surfaces before live calls, and require explicit consent for data access or writes.

## Reference(s):

- [Strava MCP repository](https://github.com/davidmosiah/strava-mcp)
- [Strava connector documentation](https://wellness.delx.ai/connectors/strava)
- [ClawHub skill page](https://clawhub.ai/davidmosiah/skills/strava-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP client stdio configuration, setup commands, safety checks, and troubleshooting guidance.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
