## Description:

Use when facing two or more independent pieces of work - separate bugs, separate subsystems, separate repos - that could be executed by concurrent agents, before dispatching any of them. Also use when the user says "fan out", "parallelize this", or hands over a pile of unrelated failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to determine whether separate coding tasks can safely run in parallel and to prepare complete, scoped assignments for concurrent agents. They use it to review returned changes together and verify the integrated result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Concurrent agents may conflict when tasks share a root cause or write to overlapping files.

Mitigation: Group work by suspected cause, confirm independence and disjoint write sets before dispatch, then review the integrated changes and rerun checks.

## Reference(s):

- [Stations on ClawHub](https://clawhub.ai/escoffier-labs/skills/skillet-stations)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Structured task assignments, triage guidance, and review checklists in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes root-cause triage, independent work, scoped assignments, and integrated review.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
