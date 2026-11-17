## Description:

Python Code Tester helps developers search project code, generate correctness-focused test cases, run tests, and repair detected issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouhh2017](https://clawhub.ai/user/zhouhh2017)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to locate target Python functions or classes, generate test cases with expected-result checks, run pytest-based validation, and summarize failures or proposed repairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan project files broadly and execute generated tests.

Mitigation: Run it only in an isolated project environment such as a disposable virtual environment or container, and confirm the exact target project path before execution.

Risk: The setup script installs Python packages from its requirements file.

Mitigation: Review the package list before running any pip install command.

Risk: The optional fix flow can update real source files.

Mitigation: Review a diff and confirm the intended target file before allowing source updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouhh2017/skills/python-code-test)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown status summaries with generated Python test code, shell command output, logs, and repair guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create test data, pytest scripts, logs, release copies, and source-code backups in the target project.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
