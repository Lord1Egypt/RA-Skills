## Description:

Converts text responses to OGG audio with Piper and sends spoken replies through Telegram when voice mode is active.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jgf78](https://clawhub.ai/user/jgf78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bot operators use this skill to convert assistant text into spoken Telegram responses and to switch between written and spoken reply modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated responses may be sent to a configured Telegram chat, exposing conversation content outside the agent environment.

Mitigation: Use only with non-sensitive content or a controlled Telegram chat, and confirm BOT_TOKEN, CHAT_ID, and voice-mode behavior before enabling spoken replies.

Risk: Audio output uses predictable shared temporary filenames, and the generated OGG file may remain after execution.

Mitigation: Run in an isolated environment and update deployment packaging to use private per-run temporary files with full cleanup before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jgf78/skills/tts-responder)
- [OpenClaw skills homepage](https://github.com/openclaw/skills)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash commands; runtime output includes OGG audio and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Piper and ffmpeg; can send generated voice messages through Telegram when BOT_TOKEN and CHAT_ID are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
