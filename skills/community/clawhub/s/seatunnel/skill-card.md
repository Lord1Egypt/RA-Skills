## Description: <br>
Apache SeaTunnel 数据集成工具助手 - 当用户需要配置、调试或生成 SeaTunnel 数据同步作业时使用此技能。支持 100+ 连接器配置、CDC 设置、性能调优和故障排查。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyzn](https://clawhub.ai/user/cyzn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to design, generate, debug, and optimize Apache SeaTunnel data integration jobs, including batch, streaming, and CDC pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example database credentials, hostnames, and CDC settings could be copied into real environments without appropriate hardening. <br>
Mitigation: Use environment variables or a secrets manager, least-privilege database accounts, test environments or FakeSource first, and review CDC and sink configurations before running against production data. <br>


## Reference(s): <br>
- [Apache SeaTunnel Documentation](https://seatunnel.apache.org/docs/) <br>
- [Apache SeaTunnel Connector V2 Overview](https://seatunnel.apache.org/docs/2.3.12/connector-v2/overview) <br>
- [Apache SeaTunnel GitHub Repository](https://github.com/apache/seatunnel) <br>
- [Apache SeaTunnel Downloads](https://seatunnel.apache.org/download) <br>
- [Apache SeaTunnel Community Slack](https://the-asf.slack.com/archives/C01CB5186TL) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with HOCON, bash, and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SeaTunnel job examples, connector guidance, troubleshooting steps, and performance tuning recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
