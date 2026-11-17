## Description:

Apache SeaTunnel 数据集成工具助手 - 当用户需要配置、调试或生成 SeaTunnel 数据同步作业时使用此技能，支持 100+ 连接器配置、CDC 设置、性能调优和故障排查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyzn](https://clawhub.ai/user/cyzn)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and data engineers use this skill to configure, generate, debug, and tune Apache SeaTunnel batch, streaming, and CDC data integration jobs. It provides connector examples, HOCON job patterns, runtime commands, and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example SeaTunnel configurations include placeholder usernames and passwords.

Mitigation: Replace placeholders with environment variables or secret-manager references before using generated jobs.

Risk: Generated data integration jobs can affect production sources or sinks if run without review.

Mitigation: Review generated SeaTunnel jobs, connector targets, permissions, and write behavior before running them against production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyzn/skills/seatunnel)
- [Apache SeaTunnel documentation](https://seatunnel.apache.org/docs/)
- [Apache SeaTunnel connector overview](https://seatunnel.apache.org/docs/2.3.12/connector-v2/overview)
- [Apache SeaTunnel GitHub repository](https://github.com/apache/seatunnel)
- [Apache SeaTunnel downloads](https://seatunnel.apache.org/download)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with HOCON, SQL, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include placeholder credentials that must be replaced before use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
