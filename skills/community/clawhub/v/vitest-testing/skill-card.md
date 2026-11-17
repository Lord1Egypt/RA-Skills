## Description:

Vitest testing framework patterns and best practices for writing unit tests, integration tests, configuring vitest.config, mocking with vi.mock/vi.fn, using snapshots, and setting up test coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write and review Vitest tests, mocking, snapshots, configuration, coverage, and verification gates for JavaScript and TypeScript projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Vitest and JavaScript testing trigger words may make the skill appear during ordinary testing discussions where it is not the best fit.

Mitigation: Apply the guidance only when the task involves Vitest tests, Vitest configuration, Vitest mocking, snapshots, coverage, or related verification gates.

Risk: Testing guidance can still be applied incorrectly, such as omitting await on Vitest resolves or rejects matchers and creating false-positive tests.

Mitigation: Use the included verification gates to run the project test command and check that async Vitest matchers are awaited.

## Reference(s):

- [Configuration](references/config.md)
- [Mocking Patterns](references/mocking.md)
- [Common Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no executable tool calls.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
