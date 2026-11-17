## Description:

Performs safety checks before high-risk operations to encourage permission checks, backups, sustainable resource use, and transparent handling of unclear requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markma84](https://clawhub.ai/user/markma84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as an on-demand safety checklist before destructive, high-volume, or configuration-changing operations. It helps prompt review of ownership, backups, resource impact, and honest communication when a request is risky or unclear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact describes daily automatic review behavior, but the security evidence says that trigger wording is unclear and should be treated as aspirational unless the hosting platform provides it.

Mitigation: Rely on explicit user-controlled invocation for high-risk actions and verify whether any platform-level trigger exists before depending on automatic review.

Risk: The safety guidance is written primarily in Chinese and may not be suitable for every team or workflow.

Mitigation: Install or enable the skill only when Chinese-language safety guidance fits the intended operators and review process.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown or natural-language safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; intended for explicit, on-demand review before high-risk actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
