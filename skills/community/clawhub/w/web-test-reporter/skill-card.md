## Description:

Automates functional testing of web systems with agent-browser CLI and helps generate standardized Word (.docx) test reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superchao9](https://clawhub.ai/user/superchao9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and test operators use this skill to inspect web application code when available, drive browser-based functional tests, capture screenshots, and assemble a structured functional test report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle login credentials and include them in generated reports or screenshots.

Mitigation: Use temporary least-privileged test accounts, remove hardcoded credentials from report templates, and redact secrets from reports and screenshots before sharing.

Risk: Browser-driven tests may submit, modify, or delete application data.

Mitigation: Run only against test or disposable environments and require explicit operator approval before destructive actions such as submit or delete.

Risk: Generated reports rely on local Python dependencies and editable filesystem paths.

Mitigation: Pin dependencies such as python-docx and review output paths before running the report script.

## Reference(s):

- [Report Format Specification](references/report-format.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, files]

**Output Format:** [Markdown instructions with bash command examples, screenshot naming conventions, and a Python report template for Word .docx output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to create browser screenshots and Word .docx reports; report templates should be edited to remove real credentials before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
