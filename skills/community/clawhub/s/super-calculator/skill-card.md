## Description:

A bilingual local calculator skill that helps an agent answer natural-language requests for arithmetic, finance, statistics, unit conversion, date, health, and equation calculations with calculation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaozhao111596](https://clawhub.ai/user/xiaozhao111596)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this OpenClaw skill to route everyday calculation requests to a local calculator assistant. It is suited for reference calculations involving finance, statistics, unit conversion, dates, health metrics, and equations where the agent should show formulas and steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance, exchange-rate, BMI, BMR, and calorie calculations may be estimates or based on user-provided assumptions.

Mitigation: Verify important financial or health decisions with authoritative sources before relying on the result.

Risk: Broad trigger language may route ambiguous numeric requests to the calculator skill before the user intent is clear.

Mitigation: Clarify ambiguous requests and required units, rates, dates, or formulas before calculating.

## Reference(s):

- [Formula Reference Guide](references/formulas.md)
- [ClawHub Skill Page](https://clawhub.ai/xiaozhao111596/skills/super-calculator)
- [Publisher Profile](https://clawhub.ai/user/xiaozhao111596)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text with formulas, calculation steps, numeric results, and optional Python function outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python standard-library calculation helpers; no API key requirement is described in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
