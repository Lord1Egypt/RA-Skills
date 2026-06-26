## Description: <br>
Configure TTS in OpenClaw and adapt speech output to user preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and agents use this skill to configure TTS behavior, select providers, and maintain concise voice, style, spoken-text, and avoidance preferences from user feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid TTS providers can require API keys and may incur usage costs. <br>
Mitigation: Review provider selection, API key configuration, and auto-speaking mode before enabling OpenAI or ElevenLabs TTS. <br>
Risk: Remembered voice preferences may persist after the user only intended a temporary speaking change. <br>
Mitigation: Periodically review the Voice, Style, Spoken Text, and Avoid sections and remove preferences the user does not want retained. <br>


## Reference(s): <br>
- [OpenClaw TTS Configuration](artifact/config.md) <br>
- [Criteria for Voice Preferences](artifact/criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, markdown] <br>
**Output Format:** [Markdown with YAML configuration snippets and compact preference entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; may propose TTS provider settings and concise updates to voice preference sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
