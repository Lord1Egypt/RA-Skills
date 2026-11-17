## Description:

Automatically processes videos by extracting audio, transcribing speech, generating timestamped subtitles, suggesting titles, and producing videos with burned-in subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chall2015](https://clawhub.ai/user/chall2015)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, educators, and developers use this skill to turn local video files into editable transcripts, SRT subtitles, title suggestions, and subtitled output videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and media processing can expose the user to untrusted packages or files.

Mitigation: Install in a virtual environment, prefer pinned dependency versions, and process only media and style files the user trusts.

Risk: If Whisper or faster-whisper is unavailable, the script can generate clearly labeled synthetic demo subtitles instead of real transcripts.

Mitigation: Check that Whisper is installed before relying on generated transcripts or subtitles for real content.

Risk: Transcripts and burned-in subtitle videos may reveal sensitive spoken content.

Mitigation: Keep outputs in a dedicated folder and review storage, sharing, and retention before publishing generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chall2015/skills/video-processor)
- [README.md](README.md)
- [CHANGELOG.md](CHANGELOG.md)
- [字幕后处理完整指南.md](字幕后处理完整指南.md)
- [后处理使用指南.md](后处理使用指南.md)
- [模型对比测试.md](模型对比测试.md)
- [优化指南.md](优化指南.md)
- [功能清单.md](功能清单.md)
- [subtitle_style_template.json](subtitle_style_template.json)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples; runtime scripts produce TXT transcripts, SRT subtitles, title text, JSON video metadata, WAV audio, and MP4 videos.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with FFmpeg and optional Whisper/faster-whisper models; subtitle styling is controlled by JSON configuration.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
