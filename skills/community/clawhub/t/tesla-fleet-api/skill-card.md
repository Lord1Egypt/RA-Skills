## Description:

Use when integrating with Tesla's official Fleet API to read vehicle and energy device data or issue remote commands such as HVAC preconditioning, wake, and charge controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and vehicle automation users use this skill to configure Tesla Fleet API access, manage OAuth tokens, read vehicle or energy device data, and run signed remote vehicle commands through the official API and local proxy flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Tesla OAuth access, local token storage, precise vehicle location, and command authority over a real vehicle.

Mitigation: Install only when that access is acceptable, protect local token and key files, and require explicit human confirmation before unlock, charging, climate, honk, location, or similar vehicle workflows.

Risk: Misconfigured API endpoints could route sensitive tokens or vehicle commands away from intended Tesla Fleet API hosts or the local signing proxy.

Mitigation: Restrict audience and base_url settings to Tesla Fleet API hosts or the localhost proxy, and avoid HTTP endpoints.

Risk: The private vehicle command key is stored as private-key.pem in the workspace.

Mitigation: Keep private-key.pem protected with owner-only permissions and avoid exposing it in chat, logs, or shared workspaces.

## Reference(s):

- [ClawHub Tesla Fleet API skill page](https://clawhub.ai/odrobnik/skills/tesla-fleet-api)
- [Tesla Fleet API setup guide](artifact/SETUP.md)
- [Tesla Fleet API command reference](artifact/SKILL.md)
- [Homepage from skill metadata](https://github.com/odrobnik/tesla-fleet-api-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON, Text]

**Output Format:** [Markdown guidance with shell commands, local configuration files, human-readable command output, and optional JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tesla OAuth credentials and local workspace state for tokens, vehicle cache, named places, and proxy materials.]

## Skill Version(s):

1.5.2 (source: frontmatter and server release evidence, released 2026-03-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
