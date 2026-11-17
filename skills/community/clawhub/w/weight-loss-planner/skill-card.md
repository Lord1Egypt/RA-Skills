## Description:

Generates personalized daily diet and exercise plans for weight loss using user-provided body metrics, goals, timeline, activity level, and preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create a structured weight-loss plan with body-metric calculations, meal guidance, weekly exercise scheduling, safety reminders, and phase-based adjustment suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Nutrition formulas and meal totals may be incorrect or misleading.

Mitigation: Review and correct calculations, calorie targets, macronutrient totals, and meal-template totals before use.

Risk: Weight-loss and exercise guidance may be unsuitable for users with medical conditions, medications, pregnancy, lactation, injuries, or symptoms during training.

Mitigation: Add explicit medical-risk screening, user confirmation, safe substitutions, stop conditions, and clinician-referral guidance before generating plans.

Risk: Chinese-language instructions may be misunderstood by users or agents that cannot reliably read Chinese.

Mitigation: Install only where the operating user or reviewing agent can understand the Chinese source instructions and generated guidance.

## Reference(s):

- [Weight Loss Planner on ClawHub](https://clawhub.ai/smallkeyboy/skills/weight-loss-planner)
- [Meal Plan Templates](references/meal-plans.md)
- [Exercise Plan Templates](references/exercise-plans.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown plan with BMI, BMR, TDEE, calorie targets, meal sections, weekly exercise schedule, safety reminders, and adjustment guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language, non-executable health and fitness guidance based on general formulas and templates.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
