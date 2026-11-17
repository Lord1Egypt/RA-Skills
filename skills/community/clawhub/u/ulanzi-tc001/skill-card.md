## Description:

Control the Ulanzi TC001 Pixel Clock over local HTTP to read status, toggle gadgets, and change display settings such as brightness, night mode, timezone, switch speed, and scroll speed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipeouropreto](https://clawhub.ai/user/felipeouropreto)

### License/Terms of Use:


## Use Case:

Developers and device operators use this skill to manage a Ulanzi TC001 Pixel Clock on a trusted local network, including checking status, enabling or disabling gadgets, and adjusting display and timing settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can resend a YouTube API key over plaintext local HTTP.

Mitigation: Use only on a trusted local network and avoid storing valuable API keys on the TC001 unless plaintext local exposure is acceptable.

Risk: The weather/AWTRIX command adds external and local network actions beyond basic TC001 clock control.

Mitigation: Document, scope, or remove that command before routine use, and confirm the AWTRIX and weather endpoints are expected for the deployment.

Risk: The server security verdict is suspicious because review is recommended before installation.

Mitigation: Review the skill before installing and scan it before deployment, using the server security guidance as the authoritative risk source.

## Reference(s):

- [Ulanzi TC001 local HTTP endpoints](references/tc001-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local HTTP requests to the TC001 device and optional weather/AWTRIX network actions when the corresponding command is used.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
