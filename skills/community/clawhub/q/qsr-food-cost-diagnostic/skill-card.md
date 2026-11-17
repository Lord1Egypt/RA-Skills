## Description:

Weekly food cost variance diagnostic for restaurant and franchise operators. Four-lever system that catches COGS drift weekly instead of monthly: ordering, portions, recipes, and waste.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcphersonai](https://clawhub.ai/user/mcphersonai)

### License/Terms of Use:

Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

## Use Case:

Restaurant and franchise operators, store managers, district managers, and multi-unit leaders use this skill to diagnose weekly food cost variance, identify likely root causes across ordering, portions, recipes, and waste, and choose corrective actions before losses compound.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain operational food-cost percentages, targets, root causes, actions, and follow-up dates for pattern tracking.

Mitigation: Use explicit diagnostic requests, avoid entering sensitive business details that should not be stored in memory, and review retained records according to the operator's data-handling policy.

Risk: Diagnostic recommendations could be incomplete or unsuitable if the operator provides inaccurate COGS, inventory, ordering, recipe, or waste information.

Mitigation: Validate recommendations against current store records, recipe standards, inventory counts, and manager judgment before making operational changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcphersonai/skills/qsr-food-cost-diagnostic)
- [Publisher profile](https://clawhub.ai/user/mcphersonai)
- [Observa getting started publisher notice](https://mcphersonai.com/observa/getting-started?utm_source=clawhub&utm_medium=skill&utm_campaign=observa-getting-started&utm_content=qsr-food-cost-diagnostic)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Conversational Markdown with diagnostic summaries and follow-up prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store diagnostic run records containing reported COGS, target percentage, variance, root cause, action, and follow-up date.]

## Skill Version(s):

1.0.4 (source: frontmatter, release metadata, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
