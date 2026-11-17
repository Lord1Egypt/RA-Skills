## Description:

Weight Loss Coach helps users track weight, calories, exercise, health screenshots, recipes, and takeout choices for personalized weight-management support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yijiecheng](https://clawhub.ai/user/yijiecheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a lifestyle coaching assistant for weight management, meal logging, calorie and exercise estimates, health screenshot summaries, progress check-ins, and low-calorie recipe or takeout suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to remember and accumulate sensitive health, diet, weight, and lifestyle information across sessions without clear consent, retention, or deletion controls.

Mitigation: Before use, confirm whether health data should be handled session-only or persisted, and provide users a way to review, delete, or disable stored profile and health data.

Risk: Health and fitness screenshots may contain unrelated personal details in addition to the data the user wants processed.

Mitigation: Ask users to crop or redact screenshots before upload unless they intend all visible details to be processed.

Risk: Weight-loss and nutrition guidance can be inappropriate for users with medical conditions, very low BMI, or signs of disordered eating.

Mitigation: Keep recommendations conservative, avoid medical advice, and direct users to a qualified clinician when disease, underweight goals, or eating-disorder signals appear.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yijiecheng/skills/weight-loss-coach)
- [Chinese food calorie database](references/calorie-database.md)
- [Exercise MET and calorie expenditure table](references/exercise-database.md)
- [Low-calorie recipes and takeout guide](references/recipes-and-takeout.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style conversational coaching responses with tables, lists, calorie estimates, summaries, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include food and exercise estimates, trend summaries, recipe steps, and safety reminders; outputs should not be treated as medical advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
