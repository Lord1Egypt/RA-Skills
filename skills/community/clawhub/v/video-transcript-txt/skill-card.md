## Description:

将一个或多个本地视频转写为带每段开始和结束时间的整理版 TXT。当用户要求视频转文字、视频转写、提取视频文本或字幕、批量生成带时间戳 TXT、整理视频口述内容、统计视频处理耗时时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[156554395](https://clawhub.ai/user/156554395)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to convert one or more fully downloaded local video files into timestamped TXT transcripts and to summarize per-video and batch processing duration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local command-line tools and installs or invokes Whisper through uv, creating ordinary dependency supply-chain exposure.

Mitigation: Use a pinned or preinstalled Whisper environment and run the skill only on video files and machines where these tools are acceptable.

Risk: No-overwrite behavior can be weakened in shared writable output directories by file races or unexpected existing files.

Mitigation: Use private output directories for batch work and review any overwrite request before allowing the skill to pass --force.

Risk: Automatic transcripts can misstate names, numbers, doses, or technical terms.

Mitigation: Review the generated TXT against the source video before using it for formal, medical, legal, financial, or other high-impact purposes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/156554395/skills/video-transcript-txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Timestamped TXT files plus human-readable progress and summary text with SUMMARY_JSON lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one final TXT per input video, reports video duration and processing time, uses bounded parallelism for batches, and avoids overwriting unless explicitly authorized.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
