## Description:

Generate comprehensive API smoke test suites - categorised tests for auth, CRUD, integrations, cached vs live endpoints, with summary reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create or adapt API smoke tests that validate authentication, CRUD, cached content, live endpoints, and integration workflows before releases, CI checks, or demos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The smoke-test runner can authenticate and trigger state-changing API workflows.

Mitigation: Run it only against disposable local or test environments unless live mutations are intentional.

Risk: The artifact includes demo credentials and product-specific requests.

Mitigation: Replace demo credentials with scoped test credentials and review endpoint behavior before execution.

Risk: Some live endpoint checks may create cached content, exercise integrations, or incur billable service usage.

Mitigation: Require an explicit opt-in for mutating or billable tests and disable those checks by default.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/smoke-test-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable smoke-test logic that sends HTTP requests to the target API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
