## Description:

提取视频音频，分段转写生成详细笔记和整理版，并可发送邮件通知以完成视频到笔记的工作流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fang232629](https://clawhub.ai/user/fang232629)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, educators, and agents processing course videos use this skill to extract audio, transcribe segmented video content, and produce Markdown study notes with optional completion notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes monitor and start scripts tied to a hard-coded external workspace.

Mitigation: Remove or ignore those scripts unless the target workspace is trusted and the paths have been reviewed.

Risk: Intermediate audio and transcript files may remain in tmp directories even where documentation claims cleanup.

Mitigation: Run the workflow in a dedicated video directory, review generated tmp and done folders, and delete sensitive intermediate files after use.

Risk: Completion email can include local file path metadata.

Mitigation: Configure email delivery only for trusted recipients or disable notification behavior for sensitive video paths.

Risk: The note organizer can produce notes that do not faithfully reflect the transcript.

Mitigation: Review generated Markdown against the transcript or source video before using it for study, documentation, or decision-making.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fang232629/skills/video-note-maker)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, transcript text files, shell command guidance, and local configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates tmp and done directories near the processed videos and may send completion notifications when mail or webhook settings are configured.]

## Skill Version(s):

1.0.0 (source: server release evidence and README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
