## Description:

Read Wyze sensor states for contact sensors, motion sensors, and temperature/humidity sensors through a read-only CLI that uses the unofficial wyze-node client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noelportugal](https://clawhub.ai/user/noelportugal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for current Wyze contact, motion, and climate sensor status such as whether doors are open, motion is detected, or a room's temperature and humidity are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Wyze API credentials and cached Wyze login state.

Mitigation: Keep the WYZE_ENV file limited to Wyze variables and restrict permissions on the token directory.

Risk: The skill depends on an unofficial Wyze client and endpoints that may change.

Mitigation: Prefer a pinned dependency or lockfile before relying on it in a sensitive home environment.

## Reference(s):

- [Wyze Sensors on ClawHub](https://clawhub.ai/noelportugal/skills/wyze-sensors)
- [wyze-node npm package](https://www.npmjs.com/package/wyze-node)
- [wyze-node GitHub repository](https://github.com/noelportugal/wyze-node)
- [Wyze Developer API Key Console](https://developer-api-console.wyze.com/#/apikey/view)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands and plain-text sensor readings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, Wyze API credentials, and cached Wyze login state.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
