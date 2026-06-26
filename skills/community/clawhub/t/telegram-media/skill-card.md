## Description: <br>
Send generated charts, photos, documents, and ElevenLabs TTS voice clips through Telegram using executed shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryandeangraves](https://clawhub.ai/user/ryandeangraves) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare and send rich media through Telegram, including generated market charts, files, and voice notes. It is intended for environments where Telegram and ElevenLabs credentials are configured and recipients are explicitly confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send local files or generated voice content through configured Telegram credentials to a hardcoded fallback chat. <br>
Mitigation: Set TELEGRAM_CHAT_ID to the intended destination, remove the hardcoded fallback, and require explicit confirmation of every recipient, file path, and text payload before execution. <br>
Risk: Media delivery commands may expose secrets, credentials, internal documents, or sensitive user content if used on the wrong files or prompts. <br>
Mitigation: Review payloads before sending and avoid using the skill for secrets, credentials, internal documents, or sensitive user content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryandeangraves/telegram-media) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may send files, images, and generated voice clips to Telegram when executed with configured credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
