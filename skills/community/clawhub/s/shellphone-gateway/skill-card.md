## Description:

Shellphone Gateway provides setup guidance for connecting iOS devices to self-hosted AI bots through a private WebSocket gateway with optional TTS/ASR support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loserbcc](https://clawhub.ai/user/loserbcc)

### License/Terms of Use:

MIT

## Use Case:

Developers and self-hosting users use this skill to set up an iOS-to-agent gateway, connect an iPhone to local AI bots, and configure Docker or Python startup with a QR-code connection flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path may run mutable external code through git clone, Docker Compose, or pip installation.

Mitigation: Review the gateway repository, package, and Docker Compose configuration before execution, and prefer a pinned release or audited commit.

Risk: Privacy claims may not fully account for TTS/ASR processing through ScrappyLabs.

Mitigation: Assume voice or text data may be sent to ScrappyLabs unless the publisher documents otherwise and provides a clear disable or opt-in setting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loserbcc/skills/shellphone-gateway)
- [Gateway GitHub repository](https://github.com/loserbcc/openclaw-gateway)
- [ShellPhone TestFlight beta](https://testflight.apple.com/join/BnjD4BEf)
- [ScrappyLabs](https://scrappylabs.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
