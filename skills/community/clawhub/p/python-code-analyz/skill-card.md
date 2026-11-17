## Description:

Analyzes Python code for syntax errors, security risks, performance concerns, code quality issues, and refactoring opportunities with severity-ranked findings and fix suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sujian0606-cpu](https://clawhub.ai/user/sujian0606-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Python files for syntax errors, static security findings, reliability issues, and code quality improvements. It returns prioritized P0/P1/P2/P3 findings with remediation guidance and optional JSON output for tool workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes local Python files supplied by the user.

Mitigation: Run it only on code intended for review and avoid submitting private source or secrets outside an approved environment.

Risk: The included example writes to a fixed /tmp/sample.py path, which can be unsafe on shared multi-user systems.

Mitigation: Change the example to use a private temporary path before running it in shared environments.

Risk: Publishing instructions and scripts rely on the ClawHub CLI.

Mitigation: Pin and isolate the CLI used for publishing, and review publish commands before executing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sujian0606-cpu/skills/python-code-analyz)

## Skill Output:

**Output Type(s):** [text, markdown, code, JSON, guidance]

**Output Format:** [Plain text or JSON analysis reports, with Markdown guidance and Python code suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Severity-ranked findings include line numbers, rule identifiers, and remediation suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact skill.yaml, artifact package.json, and artifact CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
