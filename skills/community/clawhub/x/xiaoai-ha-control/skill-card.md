## Description:

Controls XiaoAI speakers through Home Assistant and Xiaomi Miot for spoken announcements, text directives, URL audio playback, and an optional XiaoAI voice-to-OpenClaw bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[believe3344](https://clawhub.ai/user/believe3344)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers with Home Assistant and Xiaomi Miot setups use this skill to let agents speak through XiaoAI, send XiaoAI text commands, play URL audio, and optionally route whitelisted XiaoAI voice requests into OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional bridge can expose an unauthenticated network path into the main OpenClaw agent.

Mitigation: Bind the bridge to localhost or a trusted interface, add authentication before broader access, do not expose port 8765 publicly, and restrict the agent/tools used for bridge requests.

Risk: The skill can control XiaoAI and Home Assistant-connected smart-home behavior.

Mitigation: Run the downlink say/exec/play path first, review commands before automation, and keep bridge forwarding limited by a whitelist.

Risk: Voice transcripts, Home Assistant tokens, and bridge status or log files may contain private household data or secrets.

Mitigation: Protect `.env`, log, and status files; avoid publishing runtime files; and rotate the Home Assistant token if it is exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/believe3344/skills/xiaoai-ha-control)
- [bridge-setup.md](references/bridge-setup.md)
- [Home Assistant Installation](https://www.home-assistant.io/installation/)
- [HACS Download](https://www.hacs.xyz/docs/use/download/download/)
- [Xiaomi Miot Integration](https://github.com/al-one/hass-xiaomi-miot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on local Home Assistant entities, Xiaomi Miot behavior, and optional bridge configuration.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
