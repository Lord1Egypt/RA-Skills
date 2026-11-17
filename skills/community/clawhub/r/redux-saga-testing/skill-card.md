## Description:

Helps agents write robust Redux Saga tests using redux-saga-test-plan, runSaga, and manual generator testing patterns for Jest or Vitest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anivar](https://clawhub.ai/user/anivar)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to create behavior-focused Redux Saga tests, including integration tests, provider-based mocks, reducer integration, error-path coverage, and cancellation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned global install commands can make it harder to reproduce or review the exact skill version being used.

Mitigation: Pin the skills installer and GitHub source to a reviewed release or commit, and prefer a project-local install when global availability is not required.

Risk: Using incompatible Redux Saga testing dependencies can produce misleading or failing examples.

Mitigation: Pin redux-saga-test-plan to the documented compatible major version and keep redux-saga aligned with the documented baseline.

Risk: Generated saga tests may be brittle or incomplete if applied without project-specific review.

Mitigation: Review generated tests, mock external effects with providers, cover error and cancellation paths, and run the project's Jest or Vitest suite.

## Reference(s):

- [Redux Saga Testing on ClawHub](https://clawhub.ai/anivar/skills/redux-saga-testing)
- [Source repository](https://github.com/anivar/redux-saga-testing)
- [Author profile](https://anivar.net)
- [API Reference](references/api-reference.md)
- [Anti-Patterns](references/anti-patterns.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript or TypeScript code examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
