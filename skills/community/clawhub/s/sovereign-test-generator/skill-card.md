## Description:

Analyzes codebases and generates comprehensive test suites. Unit tests, integration tests, edge cases, mocking strategies. Supports JavaScript/TypeScript (Jest, Vitest), Python (pytest), Go, and Rust.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to analyze code and generate complete, runnable tests for public APIs, edge cases, error paths, and integration boundaries across common JavaScript, TypeScript, Python, Go, and Rust test frameworks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated tests may touch real databases, files, network clients, or business workflows if run without review.

Mitigation: Review generated tests before execution and replace live dependencies with fakes, stubs, mocks, or isolated test resources.

Risk: Generated tests can encode incorrect assumptions about expected behavior when the source code or requirements are ambiguous.

Mitigation: Have a maintainer verify assertions and edge-case expectations before merging the tests into the project.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ryudi84/skills/sovereign-test-generator)
- [Sovereign Tools Homepage](https://ryudi84.github.io/sovereign-tools/)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with complete test files, code blocks, and concise test strategy notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose test files for Jest, Vitest, pytest, Go testing/testify, and Rust test patterns.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
