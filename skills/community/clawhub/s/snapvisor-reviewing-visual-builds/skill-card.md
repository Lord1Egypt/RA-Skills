## Description:

Reviews SnapVisor screenshot differences for a build and, with the user's confirmation, files an approval or rejection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to inspect screenshot changes in a SnapVisor build and approve or reject the build after confirming their decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approving an unintended build can change the team's screenshot baselines.

Mitigation: Show the build's diffs and restate the specific decision before requesting explicit confirmation; file a review for only that build.

Risk: Screenshot comparison links are signed and short-lived.

Mitigation: Share the links for immediate review without storing or archiving them.

## Reference(s):

- [Reviewing Visual Builds on ClawHub](https://clawhub.ai/devino/skills/snapvisor-reviewing-visual-builds)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown with screenshot comparison links and review status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Approval or rejection is submitted only after explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
