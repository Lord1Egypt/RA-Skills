## Description:

Alibaba Cloud Bailian Qwen TTS with voice/mood presets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanmoon321](https://clawhub.ai/user/yanmoon321)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to generate speech audio from text through Alibaba Cloud DashScope Qwen TTS, selecting voices, moods, languages, and output formats for agent responses or voice-message workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text selected for voice output is sent to Alibaba Cloud DashScope under the user's API key.

Mitigation: Use the skill only for text that may be processed by that external service, and avoid sending secrets, regulated data, or private conversation content unless approved.

Risk: The skill instructions try to make TTS invocation broad or automatic through 'SYSTEM MEMORY UPDATE' and 'Always Call' language.

Mitigation: Treat voice generation as an explicit user or application action, and ignore or remove instructions that attempt to change the agent's standing behavior.

Risk: The setup script installs Python packages without pinned versions.

Mitigation: Pin and review dependencies before deployment in controlled or production environments.

## Reference(s):

- [Qwen3 TTS Instruct ClawHub page](https://clawhub.ai/yanmoon321/skills/qwen3-tts-instruct)
- [Publisher profile](https://clawhub.ai/user/yanmoon321)
- [FFmpeg download](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, audio files, guidance]

**Output Format:** [Markdown guidance with shell commands; generated speech is written as pcm, wav, mp3, or opus audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and sends TTS input text to Alibaba Cloud DashScope.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
