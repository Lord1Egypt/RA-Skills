## Description:

Sync your OpenClaw agent with the ScanWow iOS app. Receive high-quality OCR scans from your phone directly into your agent's workspace via a secure webhook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandons7](https://clawhub.ai/user/brandons7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect ScanWow iOS OCR output to an OpenClaw workspace through an authenticated webhook, so scanned text can be saved or processed by the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sample webhook can be exposed with a publicly known default token, allowing unauthorized remote writes.

Mitigation: Require SCANWOW_TOKEN to be set, reject placeholder tokens, and generate a strong random bearer token before exposing the endpoint.

Risk: Saving scans to the default current directory can write untrusted remote content into the agent workspace.

Mitigation: Use a dedicated SCANWOW_DIR for scan output and keep filename/path sanitization in place.

Risk: A public tunnel or proxy endpoint can receive oversized or abusive requests.

Mitigation: Place the webhook behind tunnel or proxy controls with body-size limits, request timeouts, and rate limits.

## Reference(s):

- [ScanWow Sync ClawHub release](https://clawhub.ai/brandons7/skills/scanwow-sync)
- [brandons7 ClawHub profile](https://clawhub.ai/user/brandons7)
- [ScanWow on the App Store](https://apps.apple.com/app/scanwow/id6670425738)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides webhook setup guidance, HTTPS tunnel options, and a JSON payload example.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
