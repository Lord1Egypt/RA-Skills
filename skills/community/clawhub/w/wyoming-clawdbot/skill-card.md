## Description:

Wyoming Protocol bridge for Home Assistant voice assistant integration with Clawdbot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vglafirov](https://clawhub.ai/user/vglafirov)

### License/Terms of Use:

MIT

## Use Case:

Developers and Home Assistant operators use this skill to connect Home Assistant Assist voice transcripts to a local Clawdbot agent through a Wyoming Protocol conversation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default deployment can expose a Clawdbot-powered voice service too broadly on a Home Assistant network.

Mitigation: Bind the service to 127.0.0.1 or a trusted interface, restrict the port with a firewall, and do not expose the service to untrusted LANs or the internet without authentication.

Risk: Voice transcripts and response text may contain sensitive household or personal information.

Mitigation: Remove or reduce transcript and response body logging before production use and limit access to service logs.

Risk: Shared Clawdbot configuration may grant the bridge more access than it needs.

Mitigation: Use a dedicated least-privileged Clawdbot account or configuration and mount only the required configuration read-only where possible.

Risk: Host networking and unpinned dependencies weaken deployment containment and repeatability.

Mitigation: Avoid host networking where practical and pin Python dependencies for reviewed deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vglafirov/skills/wyoming-clawdbot)
- [Home Assistant voice control](https://www.home-assistant.io/voice_control/)
- [Clawdbot](https://clawd.bot)
- [Wyoming Protocol](https://github.com/rhasspy/wyoming)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and runtime guidance for a local Wyoming Protocol bridge that forwards voice transcripts to Clawdbot and returns text responses for TTS.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
