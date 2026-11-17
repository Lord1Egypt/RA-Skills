## Description:

Validate Python project pyproject.toml files against PEP 517/621 rules for project metadata, build system, and tool configurations with detailed reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate Python project pyproject.toml files and receive actionable reports on project metadata, build-system settings, dependencies, and common tool configurations before release or CI use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable helper script runs locally against user-selected pyproject.toml files.

Mitigation: Review the included script where required, run it in the intended project workspace, and pass only the pyproject.toml files you mean to validate.

Risk: Rule-based validation can miss packaging edge cases or report issues that need project-specific judgment.

Mitigation: Use the reports as review guidance and confirm release-critical packaging decisions against CI results and authoritative Python packaging requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/pyproject-toml-validator)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and validator reports in text, JSON, or summary format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes distinguish pass, validation errors, and missing or unparsable files; strict mode can fail on any reported issue.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
