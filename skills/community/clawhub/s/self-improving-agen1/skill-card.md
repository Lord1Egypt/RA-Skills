## Description:

Generates Chinese-language daily menu recommendations and step-by-step cooking guidance from available ingredients, taste preferences, serving count, and cooking time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yequanzheng](https://clawhub.ai/user/yequanzheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan Chinese-language meals from ingredients on hand, including dish recommendations, preparation lists, cooking steps, and cooking timelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recipe and menu guidance may be unsuitable for allergies, dietary restrictions, or food-safety needs.

Mitigation: Review recommendations against the user's restrictions and food-safety requirements before cooking.

Risk: The optional helper script can save generated menu JSON to a user-specified path.

Mitigation: Use only intended output paths and review the destination before running the helper with --output.

Risk: The skill may activate on broad meal or menu-planning phrases.

Mitigation: Use it when Chinese-language meal planning is intended and redirect unrelated cooking or nutrition requests as needed.

## Reference(s):

- [Ingredient database](references/ingredients.md)
- [Recipe database](references/recipes.md)
- [ClawHub skill page](https://clawhub.ai/yequanzheng/skills/self-improving-agen1)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown menu plan with optional JSON output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dish recommendations, ingredient summaries, preparation guidance, cooking timelines, and follow-up prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
