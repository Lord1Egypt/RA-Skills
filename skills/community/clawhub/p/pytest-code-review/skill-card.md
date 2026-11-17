## Description:

Reviews pytest test code for async patterns, fixtures, parametrize, and mocking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review pytest test files and conftest fixtures for async testing, fixture design, parametrization, mocks, and line-specific findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal review use may involve reading pytest files selected by the user.

Mitigation: Scope review to the requested test files and conftest files, and cite specific file paths, lines, or pytest node IDs for findings.

Risk: Generic pytest guidance could be mistaken for a finding if the review gates are skipped.

Mitigation: Apply the skill's review gates before asserting pytest-specific issues, including async, fixture, mocking, and finding-specific evidence checks.

## Reference(s):

- [Async Testing](references/async-testing.md)
- [Fixtures](references/fixtures.md)
- [Mocking](references/mocking.md)
- [Parametrize](references/parametrize.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown review findings with cited file paths, line references, or pytest node IDs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal use involves reading the pytest files selected for review; the skill itself does not run commands or modify files.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
