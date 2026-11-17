## Description:

Run application to verify code changes meet expectations.

This skill is for research and development only.

## Publisher:

[dkgee](https://clawhub.ai/user/dkgee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run project-local application or test commands after code changes and inspect pass, fail, timeout, and captured log output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run any supplied command.

Mitigation: Use only reviewed, simple project-local test commands and do not pass untrusted text as the command.

Risk: Permission failures may lead users toward unsafe sudo or administrator retries.

Mitigation: Do not rerun failures with elevated privileges; fix project permissions or the test environment instead.

Risk: The expected_behavior value is descriptive only and does not verify semantic behavior.

Mitigation: Treat expected_behavior as a note and rely on explicit test assertions, command exit status, and reviewed logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dkgee/skills/verify-code-change)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Command-line text output with captured stdout and stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports pass or fail from the command exit code, supports a timeout parameter, and treats expected behavior as descriptive context.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
