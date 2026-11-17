## Description:

Discover, compare, and tailor recipes from available ingredients, kitchen gear, dietary goals, and taste preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamsellers](https://clawhub.ai/user/adamsellers)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn typed ingredients, kitchen photos, dietary goals, and household preferences into practical recipe options, meal plans, and shopping lists. It supports family-friendly planning, macro-aware cooking guidance, surprise meal ideas, and recipe comparison from web sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store durable nutrition goals, child-related meal constraints, household eating patterns, and kitchen setup preferences without an explicit consent step.

Mitigation: Review memory behavior before installation, disable or restrict memory where possible, and ask users before saving sensitive or household-specific food preferences.

Risk: Photo analysis and web recipe search are expected parts of the skill and may expose kitchen context, ingredients, or dietary constraints to connected tools.

Mitigation: Use photo analysis and web search only when needed for the user's request, avoid sharing unnecessary personal context, and summarize uncertain image findings conservatively.

Risk: Nutrition and macro estimates can be imprecise when users do not provide weighed ingredients, product labels, or exact portions.

Mitigation: Present nutrition values as approximate ranges and encourage exact tracking only when the user provides sufficient measurement details.

## Reference(s):

- [Photo to meal plan flow](references/photo-meal-flow.md)
- [Meal-plan mode](references/meal-plan-mode.md)
- [Preference memory](references/preference-memory.md)
- [Search patterns for recipe discovery](references/search-patterns.md)
- [Shopping list optimization](references/shopping-list-optimization.md)
- [Macro and nutrition structure](references/macros.md)
- [Food profile template](references/profile-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Analysis]

**Output Format:** [Markdown with concise bullets, short recipe plans, meal schedules, grouped shopping lists, and approximate nutrition notes when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include rough nutrition estimates, ranked recipe options, visible-versus-assumed ingredient distinctions, substitutions, and store-section shopping groups.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
