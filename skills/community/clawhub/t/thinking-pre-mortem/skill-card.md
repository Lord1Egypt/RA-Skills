## Description:

Before committing to a plan or launch, assume it already failed and reason backward through concrete causes to convert failure paths into mitigations, gates, and stop checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project leads, and agents use this skill to pressure-test substantial plans, launches, releases, and costly technical decisions before execution. It turns concrete failure scenarios into owners, verification checkpoints, stage gates, and plan changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The process can add unnecessary risk-analysis ceremony to small, reversible work.

Mitigation: Apply it to substantial or costly decisions and skip it for small reversible chores, active incidents, or cases where existing gates already cover the same failure paths.

Risk: Generic or unverifiable risks can create a false sense of control.

Mitigation: Require each top risk to include a past-tense failure scenario, necessary conditions, an owner, a verification checkpoint, and a ship or stage gate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjboudreaux/skills/thinking-pre-mortem)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown risk analysis with prioritized failure reasons, reverse paths, mitigations, and plan deltas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No tools, persistence, credential access, or hidden execution are indicated by the security evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
