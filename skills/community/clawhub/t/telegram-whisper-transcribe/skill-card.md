## Description: <br>
Standalone Telegram bot that transcribes voice messages, audio files, and video notes by sending audio directly to the OpenAI Whisper API and replying with text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xela-io](https://clawhub.ai/user/xela-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and run a dedicated Telegram transcription bot for voice messages, audio files, and video notes. The deployed bot replies with Whisper-generated transcripts without routing audio through an LLM agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The persistent Telegram bot can forward received audio to OpenAI and spend API credits. <br>
Mitigation: Use a dedicated Telegram bot token, restrict who can message or add the bot, and monitor OpenAI usage. <br>
Risk: The service depends on Telegram and OpenAI credentials, and installer arguments may expose secrets in shell history or process listings. <br>
Mitigation: Avoid passing real secrets directly on the command line when possible, keep the environment file permission-restricted, and rotate or remove keys when the bot is no longer used. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and Python/shell scripts; deployed bot replies with plain text transcripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TELEGRAM_BOT_TOKEN and OPENAI_API_KEY; runs as a persistent systemd user service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
