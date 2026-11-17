## Description:

把srt字幕文件转换成markdown笔记333

This skill is ready for commercial/non-commercial use.

## Publisher:

[fafeidou](https://clawhub.ai/user/fafeidou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to convert SRT subtitles into concise Chinese Markdown notes while preserving subtitle text and adding useful screenshot placeholders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The screenshot post-processing step may operate on the first Markdown or MP4 file found in the current directory.

Mitigation: Run the skill in a clean folder containing only the intended generated Markdown file and video file.

Risk: The skill can create Markdown/output files and may invoke ffmpeg on a local video.

Mitigation: Review the files in the working directory before running the bundled screenshot script and confirm ffmpeg execution is acceptable for the local media.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown file with optional screenshot image links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create output files and process local Markdown and MP4 files in the current directory when the bundled screenshot script is run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
