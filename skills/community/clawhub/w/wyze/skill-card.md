## Description:

Control Wyze smart-home devices, including lights, plugs, and wall switches, from an assistant through the unofficial wyze-node API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noelportugal](https://clawhub.ai/user/noelportugal)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Wyze smart-home devices use this skill to check and control lights, plugs, and wall switches from an assistant, including power state, brightness, color, and color temperature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control Wyze lights, plugs, and wall switches, including devices connected to physical equipment.

Mitigation: Install only when this device-control authority is acceptable, act on the user's named target, and confirm broad or sensitive actions such as turning off all devices or controlling doors, gates, heaters, or similar equipment.

Risk: The skill uses Wyze credentials, API keys, and a cached local token.

Mitigation: Use a dedicated Wyze API key and keep the environment file and token directory private.

Risk: The runtime depends on the third-party wyze-node package with a semver range.

Mitigation: Review and, where appropriate, pin or audit the wyze-node package before installation.

## Reference(s):

- [ClawHub Wyze Skill](https://clawhub.ai/noelportugal/skills/wyze)
- [noelportugal Publisher Profile](https://clawhub.ai/user/noelportugal)
- [wyze-node npm Package](https://www.npmjs.com/package/wyze-node)
- [Wyze Developer API Key Console](https://developer-api-console.wyze.com/#/apikey/view)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions and CLI command strings with plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, Wyze credentials, a Wyze API key, and a private local token cache.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
