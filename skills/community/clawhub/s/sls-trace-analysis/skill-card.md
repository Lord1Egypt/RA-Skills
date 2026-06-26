## Description: <br>
查询阿里云 SLS 日志和 ARMS 调用链，结合源码和数据库排查线上接口、用户请求和业务服务异常。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccrazyfish](https://clawhub.ai/user/ccrazyfish) <br>

### License/Terms of Use: <br>
MIT No Attribution <br>


## Use Case: <br>
Developers, SREs, and support engineers use this skill to investigate Alibaba Cloud SLS logs and ARMS traces by trace_id, wusid, or request path. It helps connect production errors to call chains, local source code, database symptoms, and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use saved Alibaba Cloud credentials to query SLS and ARMS. <br>
Mitigation: Use read-only, least-privilege credentials and scope access to the required projects, regions, and logstores. <br>
Risk: Query results can expose production logs, traces, stack data, SQL, and request or response payloads. <br>
Mitigation: Redact tokens, personal data, SQL details, stack traces, and payload fields before sharing reports outside the authorized troubleshooting context. <br>
Risk: Broad logstore selection or long time windows can retrieve more operational data than needed. <br>
Mitigation: Restrict logstores and time ranges to the smallest useful scope for each investigation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ccrazyfish/sls-trace-analysis) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown report with shell commands and JSON-derived trace and log findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include raw SLS logs, ARMS call chains, stack traces, source-code findings, database troubleshooting notes, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
