## Description:

Use when search or investigation could run forever. Set an explicit good-enough threshold first, then stop at the first option that clears it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to make bounded search and option-comparison decisions by declaring good-enough criteria before investigating. It is intended for reversible or low-stakes choices where further comparison has diminishing returns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be over-applied to correctness gates, security checks, migrations, data-loss decisions, or other high-stakes work.

Mitigation: Use the skill only for bounded, reversible, or low-stakes search; rely on required tests, security checks, and explicit review for high-stakes decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjboudreaux/skills/thinking-bounded-rationality)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Structured plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides decision, aspiration criteria, search count, selected option, residual risk, and next spend fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
