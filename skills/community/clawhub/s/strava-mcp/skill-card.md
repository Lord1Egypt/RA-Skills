## Description: <br>
Connect an MCP-compatible agent to local Strava activities, streams, routes, athlete stats, gear, and clubs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install, configure, and troubleshoot Strava MCP for MCP-compatible agents while reviewing safety and privacy boundaries before live provider access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth tokens and Strava GPS/location data can expose sensitive account or location information. <br>
Mitigation: Keep tokens private, require explicit user consent for sensitive data access, and prefer connection status, manifest, privacy audit, doctor, or dry-run checks before live reads or writes. <br>
Risk: Setup uses an npm package through npx and connects an agent to a Strava account. <br>
Mitigation: Review the referenced package and project before running commands, then run it only in a trusted environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davidmosiah/strava-mcp) <br>
- [Strava Connector Docs](https://wellness.delx.ai/connectors/strava) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup guidance, safety checks, and troubleshooting prompts for Strava MCP.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
