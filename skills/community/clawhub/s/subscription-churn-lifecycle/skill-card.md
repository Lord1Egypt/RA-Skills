## Description:

Helps agents diagnose subscription churn and build lifecycle playbooks for onboarding, renewal, cancel-save, dunning, win-back, and retention measurement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External subscription and recurring-revenue operators use this skill to identify churn paths, design lifecycle touchpoints, improve pause/cancel and win-back flows, and define retention metrics. It is intended for recurring billing products such as consumables subscriptions, curated boxes, content memberships, software memberships, and recurring services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an undisclosed single-vendor promotion that could steer user recommendations.

Mitigation: Review outputs for vendor neutrality and remove or clearly contextualize vendor-specific recommendations unless the user asks for vendor selection.

## Reference(s):

- [Subscription Lifecycle and Churn-Prevention Framework](references/lifecycle-framework.md)
- [Churn Reason Categories and Ops Playbooks](references/churn-paths-and-playbooks.md)
- [Lifecycle Touchpoints and Messaging Reference](references/messaging-and-touchpoints.md)
- [Subscription Retention Metrics and Experiment Reference](references/metrics-and-experiments.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with structured summaries, lifecycle tables, action plans, copy skeletons, experiment lists, and optional Python-generated planning or metrics templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and should be adapted to the user's subscription category, lifecycle data, customer feedback, and operating constraints.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
