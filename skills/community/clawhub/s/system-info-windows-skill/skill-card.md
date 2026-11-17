## Description:

Query system information including OS, CPU, memory, and disk usage for system configuration, resource usage, performance diagnostics, and basic system information tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujintao-2021](https://clawhub.ai/user/liujintao-2021)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to inspect local host operating system, CPU, memory, and disk information during diagnostics or environment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose basic local host details to the active agent session.

Mitigation: Install and run it only when sharing OS, CPU, memory, and disk details with the agent is acceptable.

Risk: The documentation contains inconsistent install names: system-info-skill and system-info.

Mitigation: Confirm the intended ClawHub package name and use a pinned or otherwise verified installer before running install commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liujintao-2021/skills/system-info-windows-skill)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; script output can be table text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No additional dependencies; requires Python 3.6+.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
