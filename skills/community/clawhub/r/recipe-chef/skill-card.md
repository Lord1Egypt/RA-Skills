## Description: <br>
Discover, compare, and tailor recipes from available ingredients, kitchen gear, dietary goals, and taste preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamsellers](https://clawhub.ai/user/adamsellers) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn pantry items, food photos, dietary goals, and household preferences into recipe options, meal plans, shopping lists, and practical cooking steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remember stable food, nutrition, household, and child-related preferences across sessions. <br>
Mitigation: Only save durable cooking preferences that are needed for personalization, avoid sensitive medical or household details unless necessary, and review or clear remembered preferences where the agent supports it. <br>
Risk: Ingredient recognition from photos and nutrition estimates can be uncertain. <br>
Mitigation: Separate visible ingredients from pantry assumptions, label uncertain items, and present nutrition values as rough decision-useful estimates rather than exact measurements. <br>


## Reference(s): <br>
- [Recipe Chef ClawHub page](https://clawhub.ai/adamsellers/recipe-chef) <br>
- [Profile template](references/profile-template.md) <br>
- [Search patterns for recipe discovery](references/search-patterns.md) <br>
- [Photo to meal plan flow](references/photo-meal-flow.md) <br>
- [Meal-plan mode](references/meal-plan-mode.md) <br>
- [Preference memory](references/preference-memory.md) <br>
- [Shopping list optimization](references/shopping-list-optimization.md) <br>
- [Macro and nutrition structure](references/macros.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with concise bullets, meal plans, recipe steps, shopping lists, and rough nutrition estimates when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include image-grounded ingredient confidence buckets and approximate macro ranges; does not provide medical nutrition advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
