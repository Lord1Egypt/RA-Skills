## Description:

Telegram Whisper Transcribe runs a standalone Telegram bot that transcribes voice messages, audio files, and video notes through the OpenAI Whisper API and replies with the transcript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xela-io](https://clawhub.ai/user/xela-io)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy a dedicated Telegram transcription bot that sends Telegram audio directly to OpenAI Whisper and returns text replies without LLM orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reachable Telegram bot can let unauthorized users consume the operator's OpenAI credits.

Mitigation: Add a Telegram user or chat allowlist and rate limits before exposing the bot.

Risk: Telegram audio is uploaded to OpenAI for transcription.

Mitigation: Inform users before use and avoid sending audio that should not be processed by OpenAI.

Risk: The bot depends on sensitive Telegram and OpenAI credentials.

Mitigation: Use a dedicated OpenAI key with spending limits, avoid passing real secrets on the command line, and protect ~/transcribe-bot/.env as sensitive.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash code blocks and supporting Python and shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TELEGRAM_BOT_TOKEN and OPENAI_API_KEY environment variables; produces a persistent systemd user service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
