## Description:

Reads Warzone game state and map details from war.app and scouts player statistics through a signed-in browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Warzone players and analysts use it to inspect game state, map details, and player records from a shell when the warapp-mcp server is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses your WARAPP credentials to query war.app, and the security review says some files were only partially inspected.

Mitigation: Review the skill's credential and network access before installing it, and keep the API token in a protected environment variable or dotenv file.

## Reference(s):

- [war.app GameFeed API](https://war.app/API/GameFeed)
- [fpx on npm](https://www.npmjs.com/package/@fetchproxy/cli)
- [war.app skill release](https://clawhub.ai/chrischall/skills/warapp-api)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON, tab-separated text, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only game and player data; results depend on the requested game or player.]

## Skill Version(s):

0.5.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
