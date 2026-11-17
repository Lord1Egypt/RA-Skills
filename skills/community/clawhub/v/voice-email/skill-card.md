## Description:

Send emails via natural voice commands - designed for accessibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sundiver1](https://clawhub.ai/user/sundiver1)

### License/Terms of Use:


## Use Case:

External users and accessibility-focused operators use this skill to send Gmail messages from structured voice commands received through Telegram and transcribed with Deepgram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send Gmail messages from voice transcription without a documented pre-send confirmation step.

Mitigation: Require explicit confirmation that displays the parsed recipient, subject, and body before sending any email.

Risk: The skill uses Gmail OAuth and third-party provider keys that may be stored in local configuration or key storage.

Mitigation: Use a dedicated Gmail account, low-quota provider keys, and protect openclaw.json and any configuration backups.

Risk: Setup guidance includes global package installation and external binaries.

Mitigation: Prefer a pinned or isolated install path where possible, and verify external binary sources and checksums before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sundiver1/skills/voice-email)
- [Publisher profile](https://clawhub.ai/user/sundiver1)
- [gogcli](https://gogcli.ai)
- [Deepgram console](https://console.deepgram.com)
- [Deepgram listen API endpoint](https://api.deepgram.com/v1/listen)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline command and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agent behavior for voice transcription, command parsing, Gmail sending, and setup validation.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
