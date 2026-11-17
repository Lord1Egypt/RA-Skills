## Description:

Provides Ziwei Doushu chart data for an agent to support fortune and destiny analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[letswinone888](https://clawhub.ai/user/letswinone888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request Ziwei Doushu charting data from myfate.ai, including lunar-to-solar conversion, natal charts, period fortunes, and decade ranges. The agent uses the returned data to produce clear, balanced fortune interpretations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal birth date, birth time, calendar details, gender, and an API key to an external service.

Mitigation: Use the skill only when the user accepts that data sharing, and avoid sending unnecessary personal details.

Risk: The skill includes a payment or recharge retry workflow after quota errors.

Mitigation: Before retrying after recharge, show the fields that will be resent and obtain explicit user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/letswinone888/skills/ziwei-doushu-2)
- [Publisher profile](https://clawhub.ai/user/letswinone888)
- [Skill homepage](https://skill.myfate.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline curl command examples and prose guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MYFATE_AI_API_KEY and curl; API calls send birth date, birth time, calendar details, and gender to skill.myfate.ai.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
