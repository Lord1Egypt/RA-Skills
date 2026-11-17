## Description:

Generates comprehensive, requirement-driven test cases from PRD documents or user requirements, covering functional, edge case, error handling, and state transition scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and product teams use this skill to turn PRDs or user requirements into structured, traceable test documentation. It helps plan coverage across normal flows, edge cases, error handling, and state transitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read PRD or requirement files selected by the user, which could contain sensitive product information.

Mitigation: Point the agent only to intended source files and review generated test documentation before sharing it.

Risk: The skill writes generated markdown under tests/, which could overwrite or place files in an unintended path.

Mitigation: Ask the agent to confirm the target path and avoid overwriting existing files before writing output.

## Reference(s):

- [Testing Principles and Best Practices](references/testing-principles.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown test case document with a brief text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated test cases to tests/<name>-test-cases.md and summarizes coverage, assumptions, and the output path.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
