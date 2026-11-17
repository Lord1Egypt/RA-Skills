## Description:

Turn current fridge ingredients, household size, dietary restrictions, and cooking skill level into a weekly menu that identifies needed purchases, batch-prep opportunities, and ingredient substitutions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn a list of available ingredients into a practical weekly meal plan, shopping list, batch-prep suggestions, substitutions, and waste-reduction reminders. It is especially useful when the user wants to prioritize perishable ingredients and avoid unsafe or allergy-conflicting recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad food-related phrases when the user only wants a short answer.

Mitigation: Confirm whether the user wants a weekly menu before producing the full structured plan.

Risk: Meal suggestions can become unsafe if spoiled ingredients or allergy constraints are ignored.

Mitigation: Discard suspected spoiled ingredients, avoid all user-provided allergens throughout the plan, and surface these checks in the output.

Risk: Users may ask for disease-specific diet planning beyond the skill's scope.

Mitigation: Provide only general meal-planning support and direct users to a doctor or nutrition professional for medical or nutrition prescriptions.

Risk: The bundled output template is Chinese, which may not match every user's language preference.

Mitigation: Tell the user the default output language and adapt the final menu language when they request another language.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/liuyuming0823/ym-fridge-weekly-menu)
- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-fridge-weekly-menu)
- [Food storage guide](references/storage-guide.md)
- [Ingredient substitution library](references/substitution-library.md)
- [Weekly menu template](templates/menu-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with tables and bullet lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese weekly menu structure with ingredient priority, shopping list, batch-prep suggestions, substitution table, and food-waste reminders.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
