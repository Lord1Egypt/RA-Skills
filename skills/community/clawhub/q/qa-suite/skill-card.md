## Description:

Provides project-aware testing strategy, environment guidance, interaction test plans, and integration and E2E execution with a QA report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fize](https://clawhub.ai/user/fize)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to choose and plan tests for a project, inspect its existing test setup, and prepare or run integration and end-to-end tests. It produces a QA report with coverage and results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tests may change data when run against targets that are not clearly restricted to an approved isolated environment.

Mitigation: Run only against explicitly approved local or staging targets with disposable data and dedicated test accounts; authorize execution after planning and bind test services to loopback.

Risk: Coverage uploads may disclose project or test information.

Mitigation: Review Codecov uploads before enabling them.

Risk: The bundled QA gate verdict may not establish coverage or failure evidence on its own.

Mitigation: Independently check coverage and failure evidence instead of relying only on the gate verdict.

## Reference(s):

- [Test type selection](artifact/references/test-types.md)
- [Environment inspection](artifact/references/environment-inspection.md)
- [Interaction test planning](artifact/references/interaction-test-plan.md)
- [Integration test execution](artifact/references/integration-test-execution.md)
- [E2E test execution](artifact/references/e2e-test-execution.md)
- [CI integration](artifact/references/ci-integration.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with tables, shell commands, test plans, and QA reports; may include test code and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific recommendations and execution results; unit test execution is referred to coding-tactics.]

## Skill Version(s):

1.0.0 (source: server-resolved release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
