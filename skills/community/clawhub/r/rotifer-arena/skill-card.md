## Description:

Helps developers compare Rotifer Genes through Arena evaluations and produce a Markdown report with fitness and security grades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoba-dev](https://clawhub.ai/user/xiaoba-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to import, compile, and compare Rotifer Genes or Agents in the Arena, then review a Markdown evaluation report. It requires the Rotifer CLI and keeps opponent selection and report saving under user control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The described workflow writes project and CLI state and makes public API queries.

Mitigation: Review the proposed commands, write locations, and API use before approving execution.

Risk: The security assessment is partial: a local path-like reference was unresolved, and a purpose mismatch was reported.

Mitigation: Review the unresolved reference and confirm that the popularity and download commands fit the benchmarking task before installation or use.

## Reference(s):

- [Rotifer Protocol](https://rotifer.dev)
- [Rotifer documentation](https://rotifer.dev/docs)
- [Protocol specification](https://github.com/rotifer-protocol/rotifer-spec)
- [ClawHub release page](https://clawhub.ai/xiaoba-dev/skills/rotifer-arena)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown evaluation report with comparison tables and reproduction commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports F(g) fitness and V(g) security grades when the corresponding CLI evaluations are run.]

## Skill Version(s):

1.2.11 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
