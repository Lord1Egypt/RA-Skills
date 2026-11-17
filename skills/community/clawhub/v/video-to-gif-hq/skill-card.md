## Description:

Converts video files or clips into animated GIF or WebP files with ffmpeg, including trimming, resizing, fps control, palette generation, and size optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiwei26](https://clawhub.ai/user/xiwei26)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and support teams use this skill to turn local video files or short clips into shareable animated GIF or WebP files with controlled size and quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Existing files can be overwritten at the selected output path.

Mitigation: Choose output paths deliberately and confirm before reusing an existing filename.

Risk: Large or long videos can consume significant CPU time and disk space during conversion.

Mitigation: Use shorter clips, smaller dimensions, lower frame rates, or fewer colors for large videos.

Risk: The skill processes local video files selected by the user.

Mitigation: Run it only on intended local files and avoid processing sensitive media unless local conversion is acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown response with shell command snippets and generated GIF/WebP file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local ffmpeg and ffprobe; output is a GIF or WebP file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
