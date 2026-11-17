## Description:

Use when reviewing a local video visually with systematic timestamped frame sampling, contact sheets, selected full-dimension frames, or dense inspection of a short interval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theangrypit](https://clawhub.ai/user/theangrypit)

### License/Terms of Use:

MIT

## Use Case:

Developers and reviewers use this skill to inspect local video clips with repeatable timestamped samples, contact sheets, and selected full-dimension frames while documenting coverage and audio limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Damaged or untrusted footage can cause processing to stall.

Mitigation: Use an external execution timeout and resource limits; choose a fresh output folder and allow space for decoded images.

Risk: Review files contain video imagery and the source path.

Mitigation: Review the generated files and their contents before sharing them.

## Reference(s):

- [Video Frame Review on ClawHub](https://clawhub.ai/theangrypit/skills/video-frame-review)

## Skill Output:

**Output Type(s):** [Images, JSON]

**Output Format:** [PNG contact sheets and selected full-dimension frames, plus a JSON manifest]

**Output Parameters:** [Local video path, coverage window, sampling interval, optional dense intervals and full-frame timestamps, and output directory]

**Other Properties Related to Output:** [Offline visual evidence only; the source video is not edited and audio is not reviewed. Sampling may miss events between frames or outside the selected coverage.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
