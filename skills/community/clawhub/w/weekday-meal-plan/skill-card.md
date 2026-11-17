## Description:

Plan varied weekday dinners with a pantry-first shopping list, whole-pack costs, leftovers, and an explicit budget check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkng-git](https://clawhub.ai/user/kkng-git)

### License/Terms of Use:

MIT-0

## Use Case:

Meal planners use this agent to draft weekday dinner menus and shopping lists that account for pantry stock, whole-pack quantities, leftovers, and a stated budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scan coverage was partial because a referenced memory preferences path could not be matched.

Mitigation: Review the preference-reading behavior and confirm the expected workspace path before relying on saved meal-style preferences.

## Reference(s):

- [Planning catalog (fictional prices and recipes)](references/catalog.json)
- [Weekday meal plan on ClawHub](https://clawhub.ai/kkng-git/skills/weekday-meal-plan)
- [Publisher profile: kkng-git](https://clawhub.ai/user/kkng-git)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown with menu and shopping tables, budget summary, and leftovers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A proposed plan using fictional catalog prices; it does not place orders or save preferences.]

## Skill Version(s):

0.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
