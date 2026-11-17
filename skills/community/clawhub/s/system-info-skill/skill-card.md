## Description:

Query local system information including OS, CPU, memory, and disk usage for basic diagnostics and configuration checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujintao-2021](https://clawhub.ai/user/liujintao-2021)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and support users use this skill to inspect basic local machine configuration and resource usage during troubleshooting or environment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer names differ across files, which could cause users to install the wrong package.

Mitigation: Confirm the intended package name before installation and prefer a pinned or reviewed installer command in sensitive environments.

Risk: Running the script prints basic local machine details such as OS version, CPU count, memory, and disk usage.

Mitigation: Run it only in contexts where displaying these local system details in terminal output is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liujintao-2021/skills/system-info-skill)
- [Publisher profile](https://clawhub.ai/user/liujintao-2021)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime output is table text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime output may include OS version, CPU count, memory usage, and disk usage from the local machine.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
