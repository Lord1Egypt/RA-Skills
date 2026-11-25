## Description:

Compares self-drive routes by fuel, toll, time, and fatigue costs, then recommends a route and can prepare holiday toll-window schedules and multi-day budgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengjianli0721](https://clawhub.ai/user/fengjianli0721)

### License/Terms of Use:

MIT-0

## Use Case:

External self-drive travelers use the skill to compare candidate routes on a shared cost basis, including fuel, tolls, time, and fatigue. They can also use it to plan holiday toll-window timing and multi-day trip budgets from supplied route and travel data.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security review reports a mismatch between some advertised holiday and multi-day planning features and what the code implements, and the scan was partial because a local reference could not be resolved.

Mitigation: Check applicable recommendations against the included planning guidance and current official travel information before relying on holiday timing or multi-day plans.

Risk: The security guidance reports file-reading capability without a declared tool scope.

Mitigation: Review any requested file access before installation or execution, and provide only the route inputs needed for the task.

## Reference(s):

- [Cost model](artifact/references/cost-model.md)
- [Route decision rules](artifact/references/route-decision.md)
- [Holiday toll window](artifact/references/holiday-window.md)
- [Itinerary and budget template](artifact/references/itinerary-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown recommendation with route cost tables, formulas, and applicable schedules or budgets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically up to 1,200 words and 2–4 tables; holiday schedules and multi-day budgets are included when relevant.]

## Skill Version(s):

1.0.1 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
