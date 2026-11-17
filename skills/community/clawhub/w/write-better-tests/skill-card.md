## Description:

Use when Codex is adding, editing, selecting, reviewing, or explaining tests in any repository, including mocks, fixtures, snapshots, CI validation, regression coverage, TDD/red-green proof, or readiness claims. Enforces behavior-first test design so tests catch real regressions instead of merely passing the current implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vyctorbrzezowski](https://clawhub.ai/user/vyctorbrzezowski)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when writing, revising, selecting, reviewing, or explaining tests so coverage is grounded in observable behavior and credible regression proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temporary red-green proof changes could be left in the final diff.

Mitigation: Remove temporary mutations or reverts, then rerun the focused test command before reporting completion.

Risk: Test guidance could still produce misleading confidence if the asserted boundary is too narrow.

Mitigation: Review tests against observable behavior, known test smells, and the specific regression thesis before relying on the result.

## Reference(s):

- [Test Smell Reference](references/test-smells.md)
- [ClawHub skill page](https://clawhub.ai/vyctorbrzezowski/skills/write-better-tests)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text with repository-native code and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend focused test runs, red-green proof steps, and concise final testing reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
