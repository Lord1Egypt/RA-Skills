## Description: <br>
Voice communication via Telegram that transcribes incoming voice messages with faster-whisper and replies with TTS voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Polityang](https://clawhub.ai/user/Polityang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to handle Telegram voice interactions by transcribing incoming .ogg voice messages and sending spoken replies through configured TTS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram voice messages and TTS replies may contain sensitive spoken content. <br>
Mitigation: Review Telegram and TTS privacy settings before use, and only enable the skill for conversations where voice processing is appropriate. <br>
Risk: Installing faster-whisper without a pinned trusted version can change transcription behavior or dependency exposure over time. <br>
Mitigation: Install faster-whisper from a trusted source with an explicit version pin. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Polityang/telegram-voice) <br>
- [Publisher Profile](https://clawhub.ai/user/Polityang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires faster-whisper and a configured Telegram TTS path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
