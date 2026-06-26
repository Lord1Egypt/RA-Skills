## Description: <br>
Generates daily menu recommendations from available ingredients, taste preferences, diner count, and cooking time, then returns a complete meal plan with step-by-step cooking guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yequanzheng](https://clawhub.ai/user/yequanzheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn available food ingredients and preferences into practical home-cooking menu recommendations, preparation lists, and cooking timelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask about dietary preferences, restrictions, or allergies to tailor menu recommendations. <br>
Mitigation: Share only the dietary details needed for the recommendation, and review ingredient suggestions against known allergies before cooking. <br>
Risk: The optional Python helper can write a local JSON output file when invoked with an output path. <br>
Mitigation: Run the helper only when local menu generation is intended, and choose an output path that is appropriate for generated recipe data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yequanzheng/self-improving-agen1) <br>
- [Publisher profile](https://clawhub.ai/user/yequanzheng) <br>
- [Ingredient database](artifact/references/ingredients.md) <br>
- [Recipe database](artifact/references/recipes.md) <br>
- [Evaluation scenarios](artifact/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown meal recommendations and optional JSON from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include dish recommendations, ingredient summaries, cooking steps, cooking timelines, allergy or dietary considerations, and optional local JSON files when the helper script is run with an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
