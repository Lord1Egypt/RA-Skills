## Description:

Calculate SLO/SLA error budgets, allowed downtime, burn rates, and uptime metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to calculate SLO/SLA error budgets, allowed downtime, burn rates, observed uptime, and comparisons across common availability targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Availability or uptime wording may invoke this skill for advisory SLO/SLA calculations where service-specific assumptions matter.

Mitigation: Review the input period, SLO target, and resulting budget or burn-rate output before using the calculation in operational or contractual decisions.

## Reference(s):

- [Slo Calculator on ClawHub](https://clawhub.ai/charlie-morrison/skills/slo-calculator)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Text, JSON, or Markdown calculation results with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure Python standard-library calculator; supports budget, burn, compare, uptime, multi-window, and table commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
