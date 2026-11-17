## Description:

Builds, reviews, and troubleshoots Sendly welcome, drip, and onboarding email workflows, creating new workflows disabled by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Sendly users and lifecycle marketers use this skill to plan and create onboarding email sequences, explain existing workflows, and diagnose why messages are not sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enabling or modifying a live workflow may affect emails sent to real customers.

Mitigation: Create new workflows disabled and obtain explicit user approval before enabling or changing a live workflow.

Risk: A connected Sendly account may grant broader workflow access than intended.

Mitigation: Connect with OAuth scopes matching only the workflows the user intends to manage.

## Reference(s):

- [Building Onboarding Workflows on ClawHub](https://clawhub.ai/devino/skills/sendly-building-onboarding-workflows)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a workflow trigger, numbered steps, workflow ID, and troubleshooting findings.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
