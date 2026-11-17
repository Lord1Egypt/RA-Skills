## Description:

Helps users shorten talking-head videos with Yaps Auto Cut, review pause-based edits, and export the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

Video editors and creators use this skill to remove pauses from a talking-head recording, review the cut plan, and export a shortened video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can access Yaps operations beyond Auto Cut, including transcription.

Mitigation: Limit use to the requested Auto Cut workflow and do not authorize unrelated Yaps operations.

Risk: Local video processing accesses selected files and may prompt for account credentials or permissions.

Mitigation: Select only intended files, inspect output paths before rendering, and decline unexpected Keychain prompts.

Risk: Overly aggressive pause removal can cut speech or produce an unusable edit.

Mitigation: Review the cut plan, listen at cut boundaries, and verify the exported video before use.

## Reference(s):

- [Yaps video clipping release](https://clawhub.ai/yaps/skills/yaps-video-clipping)
- [Local Yaps runtime guide](references/runtime.md)
- [Download Yaps](https://yaps.ai/download)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance and a locally exported MP4 video]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports cut metrics and the output path; review playback and speech boundaries before accepting the edit.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
