## Description:

Send generated charts, photos, documents, and ElevenLabs TTS voice clips through Telegram using executed shell commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryandeangraves](https://clawhub.ai/user/ryandeangraves)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to generate and send charts, images, documents, and voice notes to a configured Telegram chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send local files or generated media to an external Telegram chat.

Mitigation: Use only in an intentionally configured environment and restrict uploads to approved generated output directories.

Risk: The skill relies on bot and text-to-speech credentials for external API calls.

Mitigation: Keep Telegram and ElevenLabs credentials in environment configuration, rotate them if exposed, and review recipients before sending.

Risk: Inline shell and Python snippets may execute network sends without sufficient safeguards.

Mitigation: Review commands before execution, require confirmation before external sends, and prefer validated scripts or structured arguments in safer versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryandeangraves/skills/telegram-media)
- [ClawHub publisher profile](https://clawhub.ai/user/ryandeangraves)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate external Telegram and ElevenLabs API calls when commands are executed in a configured environment.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
