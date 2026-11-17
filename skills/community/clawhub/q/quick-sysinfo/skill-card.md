## Description:

快速查询本机系统信息和 OpenClaw 配置，包括 CPU、内存、磁盘、网络、环境、硬件资源、Docker 容器以及 OpenClaw 配置、频道、插件和服务状态。

This skill is ready for commercial/non-commercial use.

## Publisher:

[evangeliona](https://clawhub.ai/user/evangeliona)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local system status and OpenClaw runtime configuration during troubleshooting or environment checks. It is intended for trusted diagnostic contexts where host and configuration details may be discussed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose sensitive host details and OpenClaw configuration metadata in chats or logs.

Mitigation: Use it only in trusted diagnostic sessions and avoid sharing broad default or OpenClaw module output with untrusted recipients.

Risk: The security evidence warns that OpenClaw configuration can be exposed too easily even with redaction behavior present.

Mitigation: Review generated output before forwarding it and consider narrowing requested modules to the specific system area being diagnosed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evangeliona/skills/quick-sysinfo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown summaries of shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local IP addresses, process details, Docker ports, OpenClaw channel and plugin metadata, agent names, and redacted OpenClaw configuration values.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
