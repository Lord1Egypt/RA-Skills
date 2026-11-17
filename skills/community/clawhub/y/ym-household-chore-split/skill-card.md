## Description:

Builds rotating household chore schedules from member availability, abilities, preferences, and housing details, with workload estimates, conflict rules, and a fridge-ready Markdown chart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn household or roommate chore constraints into a balanced rotating schedule. It is intended for chore-splitting requests such as assigning tasks, estimating weekly workload, handling missed chores, and producing a Markdown chart that can be posted or shared.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad chore-related phrases and produce household planning guidance when the user only intended a brief answer.

Mitigation: Confirm the user wants a chore schedule before collecting detailed household inputs or producing the full chart.

Risk: Household availability, preferences, children, roommates, and conflict details can be sensitive.

Mitigation: Ask only for details needed to build the schedule, use nicknames or member labels, and avoid requesting personal identifiers.

Risk: Workload estimates and task assignments can be perceived as judgmental or unfair if framed as personal evaluation.

Mitigation: Present estimates as approximate, explain allocation rationale, avoid lazy or hardworking labels, and use the 30% workload-gap check to adjust or document constraints.

Risk: Unsafe assignments may be suggested for children or older household members if task constraints are omitted.

Mitigation: When children, older adults, or limited-mobility members are included, assign only safe, light tasks and exclude high, heavy, strong-cleaner, gas, and other hazardous chores.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-household-chore-split)
- [Server-resolved source repository](https://github.com/liuyuming0823/ym-household-chore-split)
- [Chore library and conflict rule template](artifact/references/chore-library.md)
- [Chore chart template](artifact/templates/chore-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown with chore lists, rationale, schedule tables, workload estimates, conflict rules, and a copy-ready chart]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only output; no networking, local file access, reminders, or persistence were found in the inspected artifact.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
