## Description:

Guides agents to convert TTS audio into Telegram-compatible OGG/Opus voice messages and send them with the correct voice-message parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shynloc](https://clawhub.ai/user/shynloc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistants use this skill to generate, convert, validate, and send Telegram voice messages from TTS output while avoiding common format, parameter, and URL-expiration errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runnable scripts and examples could allow command execution or unauthenticated message sending.

Mitigation: Review and harden scripts before use, remove unsafe webhook, remote config, eval, shell=True, and named-pipe patterns, and test in a restricted environment.

Risk: Telegram and TTS credentials can be exposed or reused across media-processing subprocesses.

Mitigation: Use scoped tokens, keep Telegram and TTS credentials separate, store secrets outside source files, and avoid passing secrets to untrusted subprocesses.

Risk: Public listeners can be abused if exposed without controls.

Mitigation: Do not expose listeners publicly unless authentication, authorization, input validation, and rate limits are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shynloc/skills/telegram-voice-message-skill)
- [Publisher profile](https://clawhub.ai/user/shynloc)
- [Telegram voice guide](docs/telegram-voice-guide.md)
- [Format requirements](docs/format-requirements.md)
- [API integration guide](docs/api-integration.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Bash, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Telegram and TTS credentials plus local media-processing tools such as ffmpeg and curl.]

## Skill Version(s):

1.0.0 (source: evidence release version and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
