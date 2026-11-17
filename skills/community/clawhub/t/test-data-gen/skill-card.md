## Description:

Generates localized test data in JSON, CSV, and MySQL/PostgreSQL SQL formats from built-in or custom templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to create sample user, order, product, review, or address records for API tests, data review, test database loading, and performance test setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL may not match the target database policy or schema expectations.

Mitigation: Review generated SQL before importing it and use least-privileged test database accounts.

Risk: Custom templates from untrusted sources may produce unsuitable or unexpected test data.

Mitigation: Use trusted templates and review custom template files before generation.

Risk: The release includes an unpinned pytest development dependency, which can affect reproducible installs.

Mitigation: Pin the dependency or remove it from production installation paths when reproducible installs matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/test-data-gen)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON, CSV, or SQL text, with optional file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports built-in templates for users, orders, products, reviews, and addresses, plus custom JSON templates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
