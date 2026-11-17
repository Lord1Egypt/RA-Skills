## Description:

Set up PostHog metrics plan with event funnel, KPI benchmarks, and kill/iterate/scale decision thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunto2](https://clawhub.ai/user/fortunto2)

### License/Terms of Use:

MIT

## Use Case:

Developers and product builders use this skill to create a PostHog metrics plan for a project, including funnel events, KPI targets, implementation snippets, and kill/iterate/scale decision thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or overwrite docs/metrics-plan.md.

Mitigation: Review the generated metrics plan before committing it, especially where analytics or business-decision guidance may be sensitive.

Risk: Default KPI thresholds and decision rules may not fit every product niche.

Mitigation: Adjust thresholds and review cadence against the project's audience, monetization model, and observed product data before using them for business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fortunto2/skills/solo-metrics-track)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown metrics plan with event tables, decision rules, and Swift or TypeScript tracking snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or updates docs/metrics-plan.md and summarizes the North Star metric, key thresholds, and first event to implement.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
