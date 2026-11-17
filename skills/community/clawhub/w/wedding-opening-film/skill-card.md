## Description:

Turns couple-supplied ceremony facts into a three-keyframe storyboard and, after approval, a wedding opening film.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Photo studios and wedding planners use this skill to plan three storyboard keyframes from confirmed ceremony details, then generate a short wedding opening film after approving paid work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorization grants broad shared Beatra access to wallet, task, and account metadata and stores a device credential locally.

Mitigation: Install only if this access is acceptable; revoke device authorization in the Beatra Console when the package is no longer trusted.

Risk: The package silently updates its own files by default.

Mitigation: Review this behavior before installation and disable automatic updates with the documented update command if desired.

Risk: Image and video generation can spend Beatra credits.

Mitigation: Review each paid generation card and its current price before approving it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/wedding-opening-film)
- [Wedding opening workflow](references/workflow.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)

## Skill Output:

**Output Type(s):** [Markdown, Images, Video]

**Output Format:** [Labeled storyboard sheet, three image keyframes, and one short video clip]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid image and video generation requires separate approvals; task results report actual charges.]

## Skill Version(s):

0.1.7 (source: server-resolved release and package manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
