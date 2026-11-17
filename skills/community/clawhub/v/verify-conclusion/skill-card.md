## Description:

Guides agents through a two-pass review of diagnostic conclusions, research findings, and inferences, with an external completeness baseline for plans and change proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rocketdemon](https://clawhub.ai/user/rocketdemon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check conclusions and proposed actions for unsupported assumptions, weak causal links, and missing coverage before acting on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting guidance may encourage disruptive checks on live services or checks that use production credentials.

Mitigation: Review proposed checks before applying them to live services; use non-production services and appropriately scoped credentials where possible. Treat the security assessment with caution because it reports uncertainty.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/rocketdemon/skills/verify-conclusion)
- [Change plan dimensions](references/change-plan-dimensions.md)
- [Common pitfalls 1–10](references/pitfalls-01-10.md)
- [Common pitfalls 11–20](references/pitfalls-11-20.md)
- [Common pitfalls 21–29](references/pitfalls-21-29.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Analysis]

**Output Format:** [Markdown with review steps, checklists, and findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A structured review based on the conclusion or plan and its available evidence]

## Skill Version(s):

1.3.1 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
