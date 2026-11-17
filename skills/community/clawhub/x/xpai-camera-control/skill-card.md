## Description:

Discover, connect, and control XPAI LAN cameras via MCP. Capabilities: device detection, streaming, WebRTC preview, snapshots, PTZ control, alarm events, illumination, image settings, detection & tracking, device management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catolin-zhang](https://clawhub.ai/user/catolin-zhang)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use the skill to discover and operate compatible IP cameras on their local network, including viewing streams, capturing or recording footage, controlling PTZ movement, and managing camera settings or event monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preview access may expose private camera feeds.

Mitigation: Use a trusted camera network and wait for fixes that restrict and authenticate preview access.

Risk: Automatic credential reuse may expose camera passwords.

Mitigation: Verify camera identity before reusing passwords, and keep credentials out of chat results and persistent relay files.

Risk: Cloud authorization, automatic session takeover, and persistent monitoring may have unexpected effects.

Mitigation: Understand these behaviors before enabling them and explicitly stop monitors when finished.

## Reference(s):

- [Camera control workflow](references/WORKFLOW.md)
- [Supported devices](references/SUPPORTED_DEVICES.md)
- [Configuration guide](references/CONFIG.md)
- [Event integration](references/EVENT_INTEGRATION.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images, Video, Stream URLs, Configuration]

**Output Format:** [Text and Markdown responses, JSON tool results, JPEG snapshots, MP4 recordings, RTSP or WebRTC stream URLs, and YAML camera configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on camera compatibility, network availability, and user authorization.]

## Skill Version(s):

1.5.6 (source: ClawHub release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
