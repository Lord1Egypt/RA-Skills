## Description:

Enforces release discipline by gating release, publish, deploy, and version-bump requests through cooldown, feedback, documentation, quality, kill-criteria, and self-contradiction checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyeuun97](https://clawhub.ai/user/gyeuun97)

### License/Terms of Use:


## Use Case:

Developers and release managers use this skill to have an agent check whether a release, deploy, publish, or version bump is ready before proceeding. It is intended to slow repeated or under-substantiated releases by requiring concrete evidence of readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may block or delay urgent release, deployment, publish, or version-bump workflows because it applies a fixed 24-hour cooldown and broad release gates.

Mitigation: Install it only where active release gating is desired, and define explicit opt-in and override rules before using it on urgent or production release workflows.

Risk: The skill records release-decision history in a persistent release log.

Mitigation: Review the release-log location and contents against team retention and sensitivity expectations before adoption.

Risk: The skill checks English documentation, SOUL.md or equivalent principles files, user feedback, and user messages, which may not match every team's release process.

Mitigation: Confirm these checks align with local release policy and adapt deployment instructions or review expectations before relying on its decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, files]

**Output Format:** [Markdown text with checklist results and release-log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce approval, warning, or blocking decisions for release actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
