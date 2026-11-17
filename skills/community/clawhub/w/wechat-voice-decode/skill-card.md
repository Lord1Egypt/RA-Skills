## Description:

WeChat Voice helps an agent identify WeChat SILK voice messages, decode them to WAV, transcribe them locally with Whisper, and respond with the recognized content or a clear status when speech is unusable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jozhn](https://clawhub.ai/user/jozhn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to process WeChat voice attachments, especially SILK audio, and turn recognized speech into text for user-facing replies. It is useful when the agent needs to distinguish successful transcription from blank, too-short, or unclear voice clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decoded voice files can remain in predictable temporary paths and may contain private or regulated information.

Mitigation: Run the skill in an isolated environment and avoid the default output path unless the script is updated to use unique temporary files and clean them up after transcription.

Risk: Python dependencies are unpinned.

Mitigation: Pin and review package versions before installing or deploying the skill.

## Reference(s):

- [Wechat Voice on ClawHub](https://clawhub.ai/jozhn/skills/wechat-voice-decode)
- [WeChat Voice Notes](references/notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain text transcription results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script prints recognized text or NO_SEGMENTS when no usable speech is detected.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
