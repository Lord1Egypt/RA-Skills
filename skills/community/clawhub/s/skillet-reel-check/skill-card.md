## Description:

Use before a rendered reel, screen-recording, demo video, or GIF goes public (social, YouTube, a landing page) to catch identity and infrastructure leaks burned into the frames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video publishers use Reel Check before publishing a reel, screen recording, demo video, or GIF to review on-screen text and recorded footage for identity or infrastructure disclosures. It guides source scanning, frame inspection, and verification after edits or re-recording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sampling frames may miss brief transitions or disclosures in audio.

Mitigation: Inspect brief transitions and audio in addition to sampled frames.

Risk: Extracted frame images may expose private information.

Mitigation: Keep extracted images private and delete them after review.

Risk: Proposed wording or attribution changes may not reflect the user's intent.

Mitigation: Review proposed wording and attribution changes before applying them.

## Reference(s):

- [Reel Check on ClawHub](https://clawhub.ai/escoffier-labs/skills/skillet-reel-check)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown review findings and actionable guidance, with optional shell and ffmpeg commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A source-text scan cannot verify rendered video or audio; manual frame and audio review is part of the workflow.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
