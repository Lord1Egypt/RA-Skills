## Description:

Analyze Sui Move test coverage, identify untested code, write missing tests, and perform security audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easonc13](https://clawhub.ai/user/easonc13)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to analyze Sui Move package coverage, identify uncalled functions, uncovered assertions, and untaken branches, then add tests and security-focused edge cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact instructs agents to stage and commit test improvements automatically.

Mitigation: Require a diff review, stage only intended files, and commit only after explicit approval.

Risk: Coverage and security suggestions may be incomplete or incorrect for a specific Move package.

Mitigation: Review generated tests and findings, then rerun Sui tests and coverage before relying on the results.

## Reference(s):

- [Sui Coverage ClawHub page](https://clawhub.ai/easonc13/skills/sui-coverage)
- [Sui CLI installation guide](https://docs.sui.io/guides/developer/getting-started/sui-install)
- [Sui Coverage GitHub repository](https://github.com/EasonC13-agent/sui-skills/tree/main/sui-coverage)
- [Sui skills repository](https://github.com/EasonC13-agent/sui-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, console text, Move test code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coverage reports may be written to files such as coverage.md; command output depends on the local Sui CLI and Move package state.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
