## Description:

Trading strategy development sandbox. User describes trading intent in natural language, agent writes a Python backtest strategy and returns results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uu-z](https://clawhub.ai/user/uu-z)

### License/Terms of Use:


## Use Case:

Developers and trading strategy builders use this skill to turn natural-language trading ideas into structured parameters, generate backtrader Python strategy code, and review backtest execution results or next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Python backtests are executed through an insecure shared temporary path and the skill describes this as a sandbox without clear containment.

Mitigation: Review before installing or running; use a private mktemp directory and explicit sandboxing before relying on the skill for repeated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uu-z/skills/trading-devbox)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language and includes parsed intent, strategy parameters, execution results, or next steps.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
