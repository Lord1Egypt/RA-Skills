## Description:

Suggest quick evening meals via AirnodeHub Spoonacular when users cannot decide what to cook after work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metobom](https://clawhub.ai/user/metobom)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get quick weekday dinner recommendations based on ingredients, time, servings, diet constraints, intolerances, dislikes, equipment, and desired effort. The skill uses AirnodeHub Spoonacular recipe data to present three practical options with concise methods and source-backed details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Food preferences, ingredients, intolerances, and diet constraints are sent to AirnodeHub Spoonacular for recipe lookup.

Mitigation: Use the skill only when users are comfortable sharing those details with the external recipe service, and avoid sending unnecessary sensitive dietary or household information.

Risk: The broad food-related trigger may activate outside explicit meal-planning requests.

Mitigation: Review trigger scope before deployment or configure agent routing so the skill is used for explicit dinner, recipe, or meal-decision requests.

Risk: Dietary and allergy safety depends on explicit user constraints and source fields returned by the recipe service.

Mitigation: Ask a concise safety question when a missing dietary constraint blocks a safe recommendation, and do not infer allergy or diet safety beyond explicit filters and returned source fields.

## Reference(s):

- [AirnodeHub Spoonacular operation contract](https://airnode-spoonacular.fly.dev/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown response with three sourced meal options, concise methods, relevant source links, and a shopping-list handoff.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recipe timing, servings, ingredients, missing ingredients, instructions, source links, and sourced protein per serving when returned by recipe data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
