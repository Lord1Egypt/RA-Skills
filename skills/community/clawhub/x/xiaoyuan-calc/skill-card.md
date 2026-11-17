## Description:

A mathematical assistant that supports scientific calculations, equation solving, inequality solving, and step-by-step calculation explanations using LaTeX input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liutengky](https://clawhub.ai/user/liutengky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and other external users can use this skill to run LaTeX-formatted mathematical calculations, solve equations and inequalities, and receive step-by-step explanations through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calculation inputs are sent to an external service and may include confidential formulas, private coursework, business data, or research values.

Mitigation: Avoid entering sensitive data and confirm that remote processing is acceptable before installing or using the skill.

Risk: Raw calculation input is logged, which may expose sensitive formulas in console output or retained execution logs.

Mitigation: Use non-sensitive inputs or remove raw input logging before deployment in environments that retain or share logs.

Risk: The skill depends on a remote calculator service, so requests may fail, stall, or return unavailable results.

Mitigation: Avoid using the skill in workflows that cannot tolerate remote-service latency or failure, and review results before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liutengky/skills/xiaoyuan-calc)
- [Xiaoyuan calculator API endpoint](https://xyst.yuanfudao.com/solar-calcbot/api/auto-solve?_productId=631)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON calculation results with text usage guidance and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LaTeX-formatted input and accepts an optional language argument.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
