## Description:

Control Alexa devices via VoiceMonkey API v2 - make announcements, trigger routines, start flows, and display media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayakumark](https://clawhub.ai/user/jayakumark)

### License/Terms of Use:


## Use Case:

Developers and automation users use this skill to prepare VoiceMonkey API requests for Alexa announcements, routine triggers, flow starts, and media display on Echo devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: VoiceMonkey tokens can be exposed when placed in URLs, logs, screenshots, or shared diagnostics.

Mitigation: Use POST requests with the Authorization header, avoid token query strings, and rotate the token if exposure is suspected.

Risk: The skill helps an agent operate VoiceMonkey-linked Alexa devices, which can create unexpected announcements or media playback.

Mitigation: Install only for intended VoiceMonkey device control and review proposed announcements, triggers, and media commands before execution.

## Reference(s):

- [VoiceMonkey skill page](https://clawhub.ai/jayakumark/skills/voicemonkey)
- [VoiceMonkey homepage](https://voicemonkey.io)
- [VoiceMonkey console](https://console.voicemonkey.io)
- [VoiceMonkey API v2](https://api-v2.voicemonkey.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and XML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a VOICEMONKEY_TOKEN environment variable and VoiceMonkey device or flow identifiers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
