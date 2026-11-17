## Description:

Plans and publishes social posts across platforms from one calendar file, reporting which posts are scheduled, due, waiting for approval or already published, and publishing approved posts when they are due. Use when the user wants a posting schedule, content calendar, or to publish queued posts at set times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social media operators use this skill to track scheduled posts, identify posts awaiting approval, and publish approved posts from a shared calendar file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Content may change after approval checks and still be published.

Mitigation: Use status and dry-run modes; before unattended publishing, require approval for an immutable snapshot and verify that approval immediately before publication.

Risk: The same approved post may be published twice, including during overlapping runs.

Mitigation: Avoid overlapping publish runs and keep unattended publishing disabled until duplicate-entry protection is in place.

Risk: Excessive connected accounts or token permissions can increase the impact of a credential problem.

Mitigation: Limit connected accounts and token permissions to what the workflow needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahmadhussain0335/skills/socialkit-content-calendar)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands]

**Output Format:** [Markdown status tables and per-entry results, with shell commands for calendar checks and publishing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports platform, post type, publish time, status, problems, and per-entry publish results or errors.]

## Skill Version(s):

0.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
