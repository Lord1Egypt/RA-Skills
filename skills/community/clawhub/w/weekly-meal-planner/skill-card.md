## Description:

Weekly Meal Planner generates a seven-day breakfast, lunch, and dinner menu plus a shopping list from household size, budget, and taste preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan weekly household meals around people count, daily budget, and taste preferences. It is oriented toward Chinese-language meal names, yuan-denominated estimates, and simple shopping-list generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Menu costs and shopping-list prices are rough estimates and may not match current local prices or nutritional needs.

Mitigation: Review and adjust the generated plan before using it for purchasing or household budgeting.

Risk: The bundled script writes menu_plan.json in the current working directory and may overwrite an existing file with that name.

Mitigation: Run the script in a directory where that output file is expected, or move any existing menu_plan.json before execution.

Risk: The skill does not detect allergies or enforce dietary restrictions.

Mitigation: Screen generated meals for allergies, medical dietary needs, and household restrictions before use.

Risk: The meal database is Chinese-oriented and uses yuan-denominated budget assumptions.

Mitigation: Use it only where those assumptions are acceptable, or adapt meal names and pricing for the intended locale.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/weekly-meal-planner)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON]

**Output Format:** [Markdown-style agent guidance, terminal output, and a menu_plan.json file when the bundled script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script creates or overwrites menu_plan.json in the current working directory.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter and _meta.json list v1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
