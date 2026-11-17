## Description:

Summarize YouTube videos with no subtitles by doing local ASR with yt-dlp and faster-whisper, then extracting optional screenshot frames with ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yifany-github](https://clawhub.ai/user/yifany-github)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to summarize YouTube videos when subtitles are missing or API keys should not be used. It guides an agent through a local download, transcription, timeline summary, and optional frame extraction workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ASR dependency is unpinned and may change behavior or introduce supply-chain risk.

Mitigation: Install in a dedicated virtual environment and review the faster-whisper package before use.

Risk: Automatic transcription can misrecognize names, numbers, or homophones, especially when the language option is wrong.

Mitigation: Set the language option deliberately and verify important details against the transcript or source video.

Risk: Extracted frames may include sensitive or copyrighted visual content.

Mitigation: Inspect generated screenshots before sharing or attaching them.

## Reference(s):

- [Workflow notes (YouTube no-subtitle)](references/workflow.md)
- [ClawHub skill page](https://clawhub.ai/yifany-github/skills/youtube-asr-summarize)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces summary.md, transcript.txt, transcript.srt, and optional JPEG frames under the selected output directory.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
