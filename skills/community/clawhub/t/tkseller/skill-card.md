## Description:

TKSeller helps an agent run an automated TikTok Shop selling workflow by logging into the TKSeller service, recommending or analyzing videos, sending review cards, and routing approval actions through chat channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanholt921](https://clawhub.ai/user/evanholt921)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants and operators use TKSeller to connect an OpenClaw agent to a selling workflow for product-video recommendations, digital-persona selection, storyboard and video review, approval, rejection, and publishing steps through chat buttons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles TKSeller passwords and persistent local tokens.

Mitigation: Install only when the publisher is trusted, avoid valuable account credentials until safer login and protected token storage are available, and clear stored tokens if access should be revoked.

Risk: The skill relies on a remote data service and the security evidence recommends waiting for HTTPS and a safer login flow.

Mitigation: Use only on trusted networks and prefer non-sensitive or test accounts until HTTPS and a safer authentication flow are supported.

Risk: The skill can access OpenClaw gateway and channel configuration and can run a background polling process that sends messages.

Mitigation: Review channel targets and gateway permissions before use, monitor background polling, and stop or remove polling when the selling workflow is complete.

## Reference(s):

- [TKSeller ClawHub Skill Page](https://clawhub.ai/evanholt921/skills/tkseller)
- [OpenClaw Discord Channel Documentation](https://docs.openclaw.ai/channels/discord)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses with inline shell commands and JSON status from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit NO_REPLY or OUTPUT_AS_REPLY-prefixed text; review and status messages can be delivered through configured chat channels and background polling.]

## Skill Version(s):

3.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
