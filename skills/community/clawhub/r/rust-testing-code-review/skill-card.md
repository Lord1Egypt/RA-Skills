## Description:

Reviews Rust test code for unit, integration, async, mocking, property-based, concurrency, and edition-specific testing patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to review Rust test files, test modules, and test infrastructure for correctness, isolation, async behavior, concurrency coverage, and maintainable assertion patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Illustrative database cleanup snippets could be harmful if applied to a non-disposable database.

Mitigation: Require a clearly disposable test database before using destructive cleanup examples.

Risk: Optional test tools used in CI or shared developer environments can drift over time.

Mitigation: Pin optional tools such as cargo-insta when adopting them in CI or shared workflows.

## Reference(s):

- [Unit Tests](references/unit-tests.md)
- [Integration Tests](references/integration-tests.md)
- [Advanced Testing](references/advanced-testing.md)
- [Concurrency Testing](references/concurrency-testing.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured code review findings with file-line references, severity labels, and concise explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires concrete review evidence before listing findings; may include Rust testing recommendations and command examples when relevant.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
