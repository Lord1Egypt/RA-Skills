## Description:

视频基础质量审核技能，对视频进行批量或单条的基础问题检测，包括画面质量、构图、音频、黑边、分辨率等，输出审核报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sgw2285265753-design](https://clawhub.ai/user/sgw2285265753-design)

### License/Terms of Use:

MIT-0

## Use Case:

Content reviewers and video operations teams use this skill for first-pass short-drama video checks covering technical quality, visual content issues, and transcript keyword screening. It produces a timestamped review report with issue severity and editing suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes both video frames and spoken content for policy categories, which can expose private or sensitive media during review.

Mitigation: Run it only on media approved for this workflow, review where extracted frames/audio are stored, and avoid sending private content to external image or transcription tools without authorization.

Risk: The security scan reports unsafe local execution patterns, including Python command interpolation and hard-coded local paths.

Mitigation: Review and fix local paths and command construction before installing or running the scripts on untrusted filenames or shared systems.

Risk: Visual checks can fail open and return passing results when tooling is unavailable, times out, or emits errors.

Mitigation: Treat clean reports as preliminary, monitor tool failures, and require human review for release decisions.

Risk: Temporary audio and extracted frame handling can leave sensitive derivatives if cleanup fails or output paths are changed.

Mitigation: Use controlled temporary directories, restrict file permissions, and delete derived frame/audio artifacts after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sgw2285265753-design/skills/video-review)
- [Publisher profile](https://clawhub.ai/user/sgw2285265753-design)
- [banned_words.json](refs/banned_words.json)

## Skill Output:

**Output Type(s):** [text, markdown, Shell commands, configuration, guidance]

**Output Format:** [Markdown report with timestamped findings, severity labels, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also write local JSON or text reports when scripts are run with output paths.]

## Skill Version(s):

1.0.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
