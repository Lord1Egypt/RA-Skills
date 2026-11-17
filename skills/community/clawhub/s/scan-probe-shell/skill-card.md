## Description:

Turn a list of raw commit notes or release bullet points into a clean, user-facing changelog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liang030214](https://clawhub.ai/user/liang030214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support staff, and project managers use the skill to turn rough release notes into a clear summary of user-visible changes for a release page or store listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied release notes may contain sensitive information.

Mitigation: Share only notes appropriate for the agent's normal data handling practices.

Risk: Rewriting technical notes can introduce claims that overstate what a change does.

Mitigation: Check each generated claim against the source notes before publishing.

## Reference(s):

- [Changelog Writer on ClawHub](https://clawhub.ai/liang030214/skills/scan-probe-shell)

## Skill Output:

**Output Type(s):** [Markdown]

**Output Format:** [Markdown with headings and bullets grouped by change type]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise, user-facing release notes; omits changes without a user-visible effect.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
