## Description:

Merges numerically prefixed MP4 clips into a single video or time-based chunks while normalizing resolution, frame rate, codec, audio, and optional fade transitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[machunlin](https://clawhub.ai/user/machunlin)

### License/Terms of Use:

MIT

## Use Case:

External creators, developers, and video production teams use this skill to batch-combine AI-generated scenes or recorded clips into finished MP4 videos or chunked outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe filename handling can expose risk when clip names or input directories are attacker supplied.

Mitigation: Use only trusted video directories and filenames, and avoid running the skill on attacker-supplied clip names.

Risk: The skill runs FFmpeg commands and the install script may use sudo or a system package manager to install FFmpeg.

Mitigation: Review install.sh before installation, inspect commands before execution, and choose output paths carefully.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/machunlin/skills/video-merger)
- [FFmpeg download](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; MP4 files are produced when the commands are executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local FFmpeg and trusted MP4 input directories and filenames.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
