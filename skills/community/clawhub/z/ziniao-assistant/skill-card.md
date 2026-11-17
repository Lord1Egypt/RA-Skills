## Description:

Controls Ziniao Browser through the local Ziniao bridge, discovers available ZClaw tools before invoking them, and requires an API key for browser actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziniao-open](https://clawhub.ai/user/ziniao-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to control Ziniao Browser stores, navigate pages, read content, interact with page elements, take screenshots, export files, and run supported browser automation through the ZClaw bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate authenticated browser sessions through the Ziniao/ZClaw bridge.

Mitigation: Install only when the bridge is trusted and limit use to intended browser stores and sessions.

Risk: The skill relies on a ZClaw API key for invoke requests.

Mitigation: Store the key in a protected secret manager or tightly permissioned environment/config file, avoid exposing it in chat or shell history, and rotate it if exposure is possible.

Risk: Changing the bridge base URL can route browser automation to an unintended or untrusted endpoint.

Mitigation: Keep the base URL on the intended local bridge unless a remote endpoint is explicitly trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziniao-open/skills/ziniao-assistant)
- [Ziniao Ecosystem Center](https://open.ziniao.com/contactUs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON request bodies, and browser automation instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce page-content summaries, browser action guidance, screenshots, downloaded files, and configuration updates when supported by the bridge.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
