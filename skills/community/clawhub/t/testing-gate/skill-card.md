## Description:

A testing gate checker for test coverage, strategy validation, and regression verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terr123123](https://clawhub.ai/user/terr123123)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill as a quality gate before merges or releases to check coverage targets, test strategy completeness, and regression status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quality-gate logic has validation and fail-open weaknesses if used as the sole merge or release gate.

Mitigation: Require all mandatory checks, validate inputs before invoking the gate, and pair results with CI test execution and coverage tooling.

Risk: Malformed or incomplete coverage, strategy, or regression artifacts can produce misleading pass/fail decisions.

Mitigation: Validate required fields, numeric ranges, and artifact completeness before running checks.

Risk: Shared TestingGate instances across concurrent jobs can mix state between workflows.

Mitigation: Use a separate TestingGate instance per job or clear state before each isolated workflow.

## Reference(s):

- [Testing Gate ClawHub skill page](https://clawhub.ai/terr123123/skills/testing-gate)
- [Publisher profile](https://clawhub.ai/user/terr123123)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces testing-gate guidance and examples for coverage, test strategy, regression checks, and release-readiness workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
