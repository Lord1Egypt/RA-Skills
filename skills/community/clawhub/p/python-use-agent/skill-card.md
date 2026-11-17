## Description:

Python Use Agent is a backward-compatible ClawHub skill that routes Python task requests toward a unified code entry point and can generate, run, review, and report on Python code tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external ClawHub users can use this skill as a compatibility layer for Python-oriented tasks such as data analysis, API calls, automation, code execution, and code review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill exposes unsandboxed host code execution while presenting sandbox and review behavior that is not actually enforced.

Mitigation: Run only trusted tasks or code, review generated code before execution, and use an external container or restricted environment when isolation is required.

Risk: Artifact behavior allows Python code execution with filesystem and network access in normal operation.

Mitigation: Avoid supplying secrets or sensitive files to the execution environment unless the hosting agent is already approved for that access.

## Reference(s):

- [Python Use Agent ClawHub listing](https://clawhub.ai/jirboy/skills/python-use-agent)
- [AiPy homepage](https://www.aipy.app/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON and text responses with generated code, execution logs, stdout, stderr, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save logs, generated code, and execution results under python-use-results.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
