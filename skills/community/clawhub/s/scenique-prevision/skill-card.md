## Description:

Scenique Prevision runs a decision-forecasting simulation using Menos architecture concepts and swarm-style agent roles to produce probabilistic scenario guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shewingong](https://clawhub.ai/user/shewingong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to explore possible outcomes for a decision or query before acting. It is suited to scenario planning where outputs should be treated as decision support rather than a deterministic recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision-forecasting output may be mistaken for a reliable prediction or instruction.

Mitigation: Treat outputs as scenario-planning support and require human review before acting on financial, operational, or other sensitive decisions.

Risk: Future gateway, memory, ledger, or subagent integrations may expose sensitive context to the simulation.

Mitigation: Confirm and limit what external OpenClaw, long-term memory, ledger, and subagent integrations can access before use with sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shewingong/skills/scenique-prevision)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or JSON-style status output with probabilistic scenario guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a decision query and an optional mode value: light, standard, or sovereign.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
