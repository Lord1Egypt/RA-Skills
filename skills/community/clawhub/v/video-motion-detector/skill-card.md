## Description:

Detects and analyzes specified motion sequences in video, including martial arts, dance, and posture changes, then reports structured results through Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hena1985](https://clawhub.ai/user/hena1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video-analysis users use this skill to download or ingest videos, extract frames, inspect motion over the full timeline, and determine whether requested action sequences, simultaneous actions, or repetition counts occurred.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloader commands may be run against user-provided video URLs without safe argument handling.

Mitigation: Use only trusted video URLs, validate URLs before download, and prefer shell-free downloader invocation where possible.

Risk: Video files, extracted frames, and analysis results may contain sensitive content and can be stored locally or sent to Feishu.

Mitigation: Confirm permission to process the video, handle local artifacts according to data-retention requirements, and verify the Feishu recipient before sending results.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured result summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include video source details, detection conditions, timestamps, pass/fail conclusions, and Feishu notification content.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
