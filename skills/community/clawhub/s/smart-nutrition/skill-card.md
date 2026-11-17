## Description:

Smart Nutrition Customizer. Input height, weight, age, gender, and activity level to calculate BMR and macronutrient needs, then generate a full-day meal plan with recipes, calorie counts, and nutrition labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to estimate BMR, TDEE, and macronutrient targets from basic body and activity data, then receive a full-day meal plan with recipes, ingredient amounts, calorie counts, and nutrition labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat calorie, macronutrient, or meal-plan estimates as medical nutrition therapy.

Mitigation: Frame outputs as general guidance and direct users with clinical needs, pregnancy, minors, eating-disorder support, diabetes, kidney disease, or other medical conditions to a qualified professional.

Risk: The skill asks for basic body and goal information that some users may consider sensitive.

Mitigation: Ask only for missing information needed for the estimate and avoid retaining it unless the host agent has an explicit privacy basis.

Risk: Allergy handling may be limited to simple avoidance.

Mitigation: Ask about allergies and dietary restrictions before planning meals, avoid identified ingredients, and advise users with serious allergies to verify labels and consult qualified support.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown with tables, recipe sections, calorie estimates, and nutrition summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided body data, activity level, health goal, dietary preferences, allergies, and optional calorie targets to produce general nutrition guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
