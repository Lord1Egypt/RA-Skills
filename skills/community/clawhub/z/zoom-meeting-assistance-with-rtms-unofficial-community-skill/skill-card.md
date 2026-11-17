## Description:

Zoom RTMS Meeting Assistant starts on demand to capture Zoom meeting audio, video, transcripts, screenshare, and chat via Real-Time Media Streams, then provides AI-powered dialog suggestions, sentiment analysis, live summaries, and WhatsApp notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanchunsiong](https://clawhub.ai/user/tanchunsiong)

### License/Terms of Use:

MIT

## Use Case:

Developers and meeting operators use this skill to receive Zoom RTMS webhooks, record meeting media and transcripts, and generate meeting summaries, sentiment analysis, and dialog suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill captures sensitive Zoom meeting audio, video, transcripts, screenshares, and chat.

Mitigation: Use only in controlled environments with clear participant consent, data-handling rules, and retention/deletion controls.

Risk: The server security summary reports unauthenticated webhook and admin endpoint risks.

Mitigation: Add Zoom webhook signature verification and authenticated admin endpoints before deployment.

Risk: The server security guidance identifies TLS and RTMS URL validation risks.

Mitigation: Require normal TLS verification and strict allowlists for RTMS URLs.

Risk: The server security guidance identifies command-injection risk around media processing.

Mitigation: Invoke ffmpeg safely without a shell and validate filenames and paths before processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanchunsiong/skills/zoom-meeting-assistance-with-rtms-unofficial-community-skill)
- [OpenClaw dependency](https://github.com/openclaw/openclaw)
- [ngrok unofficial webhook helper](https://github.com/tanchunsiong/ngrok-unofficial-webhook-skill)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, plain text, VTT/SRT transcripts, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create meeting recordings, transcripts, chat logs, event logs, AI summaries, dialog suggestions, sentiment JSON, screenshare PDFs, and converted media files when configured.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
