## Description:

Uploads a user-selected MP4 or MOV video to Wondershare-hosted Filmora cloud endpoints for AI enhancement, then downloads the enhanced result to local storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[double-ing](https://clawhub.ai/user/double-ing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to improve local MP4 or MOV video quality through Wondershare cloud processing after the user explicitly accepts uploading non-sensitive media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uploads the selected source video to Wondershare-hosted cloud endpoints.

Mitigation: Use only after explicit user consent and avoid sensitive, private, or confidential videos.

Risk: The provider receives video metadata and a stable device-level identifier during processing.

Mitigation: Disclose the metadata and device identifier before execution and proceed only when the user accepts that sharing.

Risk: Duration and resolution limits are important for successful processing.

Mitigation: Verify the input format, duration, and resolution before running the enhancement workflow.

Risk: Cloud-side deletion claims are not independently confirmed by the release evidence.

Mitigation: Do not rely on deletion claims unless Wondershare's retention terms independently confirm them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/double-ing/skills/video-enhancer)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown status text and a locally saved enhanced video file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an enhanced video file using the <input_stem>_hd_YYYYMMDD_HHMMSS.<ext> naming pattern; supports MP4 and MOV inputs and requires ffprobe.]

## Skill Version(s):

1.0.9 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
