## Description:

Control Roku devices via CLI. Discovery, remote control, app launching, search, and HTTP bridge mode for real-time control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover Roku devices on a local network, send remote-control commands, launch apps, enter text, inspect device status, and configure bridge-style control workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real remote-control commands to Roku devices on the local network.

Mitigation: Use it only with Roku devices you own or administer, and confirm the target host or saved alias before sending commands.

Risk: The release includes Telegram remote-control code that can route button callbacks into a local Roku daemon.

Mitigation: Protect the Telegram bot token, restrict who can interact with the bot, and disable the Telegram path when it is not needed.

Risk: Bridge-style control can expose Roku commands through a local HTTP service if configured carelessly.

Mitigation: Bind the bridge to localhost, use a strong bearer token, and avoid exposing the bridge port to untrusted networks.

Risk: Installation metadata uses an unpinned third-party npm package.

Mitigation: Review and pin the package version in controlled deployments before installing.

## Reference(s):

- [ClawHub Roku skill page](https://clawhub.ai/gumadeiras/skills/roku)
- [Publisher profile](https://clawhub.ai/user/gumadeiras)
- [Declared Roku CLI repository](https://github.com/gumadeiras/roku-cli)
- [python-roku library](https://github.com/jcarbaugh/python-roku)
- [npm package @gumadeiras/roku](https://www.npmjs.com/package/@gumadeiras/roku)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local network addresses, Roku command names, bridge tokens supplied by the user, and service-management commands.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
