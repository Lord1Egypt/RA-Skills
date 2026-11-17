## Description:

Multi Agent coordinates specialized planner, executor, reviewer, and coordinator roles to decompose, execute, review, and summarize complex agent tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to run multi-agent collaboration workflows for project analysis, code review, research reports, quality assurance, and debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic shell execution fallback can run task text as an operating-system command when tool matching falls through.

Mitigation: Use only in an isolated project directory with trusted task text, and remove or replace the shell fallback before shared or sensitive use.

Risk: Executor and tool roles can perform file operations or command execution if broad tools are supplied.

Mitigation: Limit filesystem and shell permissions, avoid secrets in task context, and review generated actions before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-multi-agent)
- [Skill Usage Guide](artifact/SKILL.md)
- [README](artifact/README.md)
- [Test Report](artifact/TEST_REPORT.md)
- [Fix Report](artifact/FIX_REPORT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console text and structured JavaScript result objects; configured agent roles may produce Markdown, code, configuration, shell commands, or guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by workflow mode and configured tools; review generated commands and file-writing actions before use.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
