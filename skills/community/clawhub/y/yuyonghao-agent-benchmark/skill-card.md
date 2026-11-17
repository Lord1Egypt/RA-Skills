## Description:

Agent Benchmark evaluates AI agent task-completion ability with standardized benchmark tasks for file operations, data processing, system operations, robustness, and code quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run lightweight benchmark tasks against AI agents, compare task-completion behavior, diagnose weak capability areas, and generate Markdown benchmark reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the benchmark can run supplied task code with host privileges.

Mitigation: Run it only in a disposable sandbox or container with no API keys or sensitive files available.

Risk: The security evidence identifies unsafe file path handling that can overwrite, delete, or persist data outside the expected scope.

Mitigation: Use trusted task files only, validate task IDs and CLI paths before execution, and restrict writable directories.

Risk: The artifact writes benchmark reports, temporary task files, and a memory-path report during normal operation.

Mitigation: Review generated files after each run and avoid running the skill from directories that contain important data.

Risk: The security guidance notes a mismatch between the documented PowerShell runner and the shipped executable.

Mitigation: Confirm the intended runtime and entry point before normal use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-agent-benchmark)
- [Skill documentation](artifact/SKILL.md)
- [Test summary](artifact/TEST_SUMMARY.md)
- [Benchmark report](artifact/benchmark-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, console output, task definitions, code snippets, and runner guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes benchmark reports and temporary task files during execution.]

## Skill Version(s):

0.1.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
