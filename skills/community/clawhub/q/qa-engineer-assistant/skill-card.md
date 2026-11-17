## Description:

QA Engineer Assistant helps QA and test engineers analyze requirements, design test cases, generate API and UI automation scripts, create bug reports, and guide junior testers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guolongganga](https://clawhub.ai/user/guolongganga)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, test engineers, and developers use this skill to turn requirements, API specifications, UI flows, and bug descriptions into test cases, automation code, bug reports, and testing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Python tests may be unsafe when created from endpoint descriptions supplied by untrusted people.

Mitigation: Read generated tests before running them, especially before using the API test generator with untrusted input.

Risk: Generated examples encourage editing API base URLs and test credentials into conftest.py.

Mitigation: Store API base URLs and credentials in environment variables or a secret manager instead of committing them to generated files.

Risk: Dependency installation guidance does not pin package versions.

Mitigation: Pin dependencies before using the generated test setup in CI or shared developer environments.

## Reference(s):

- [API Test Guide](references/api-test-guide.md)
- [Bug Report Template](references/bug-report-template.md)
- [Test Case Template](references/test-case-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, fenced Python code blocks, shell command snippets, and structured bug-report Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes beginner-oriented Chinese comments and next-step recommendations in generated outputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
