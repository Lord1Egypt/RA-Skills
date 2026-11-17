## Description:

Author tests that catch regressions by selecting behaviors based on risk, proving each new test can fail, mocking only external boundaries, and pinning untested legacy behavior with characterization tests before changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need an agent to add regression-focused tests, characterize legacy behavior, or improve test coverage while avoiding brittle or tautological assertions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running existing test suites can trigger repository-specific side effects.

Mitigation: Review proposed commands and run them in a controlled development environment before accepting changes.

Risk: Temporary mutation checks could leave unintended production edits if interrupted.

Mitigation: Inspect the final diff and confirm temporary mutations were reverted before accepting the test changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dennisrongo/skills/write-tests)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with code edits and shell command summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include new or edited test files, characterization notes, and quoted test run results.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
