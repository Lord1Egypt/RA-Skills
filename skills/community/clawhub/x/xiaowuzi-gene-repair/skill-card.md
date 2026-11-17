## Description:

Helps an agent monitor and repair logic errors, syntax conflicts, and instruction anomalies during AI gene-evolution workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonicpopo](https://clawhub.ai/user/tonicpopo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as an immune and repair layer for long-running automated agent workflows, especially when they want anomaly detection, rollback, and instruction repair behavior around evolving prompt or logic fragments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes unattended rollback and instruction self-repair without clear limits or approval gates.

Mitigation: Install it only where autonomous repair is intended, and define explicit limits for what state it may modify and when human confirmation is required.

Risk: The publisher trust tier is low in the server quality metadata.

Mitigation: Review the artifact and security summary before enabling it in workflows that require strict human control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tonicpopo/skills/xiaowuzi-gene-repair)
- [Publisher profile](https://clawhub.ai/user/tonicpopo)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance and agent instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose autonomous rollback or prompt/instruction repair behavior; review boundaries before deployment.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
