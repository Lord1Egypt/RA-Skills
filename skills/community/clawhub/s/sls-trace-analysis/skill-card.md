## Description:

查询阿里云 SLS 日志和 ARMS 调用链，结合源码和数据库线索进行全链路问题排查并给出修复方向。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccrazyfish](https://clawhub.ai/user/ccrazyfish)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and operations engineers use this skill to investigate Alibaba Cloud service incidents from trace_id, wusid, or path by querying SLS and ARMS, reviewing grouped logs and spans, and following up with source-code and database checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose raw production logs, stack traces, request data, response data, tokens, user identifiers, or business fields in its output.

Mitigation: Run it only for authorized incidents and redact sensitive fields before sharing reports outside the approved troubleshooting context.

Risk: Cloud credentials with broad SLS or ARMS access could allow unnecessary access to production observability data.

Mitigation: Use least-privilege Alibaba Cloud keys limited to the required projects, regions, and logstores.

Risk: Automatic source-code inspection may examine repositories outside the intended incident scope.

Mitigation: Use the skill from the relevant project workspace and review the scoped code findings before acting on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccrazyfish/skills/sls-trace-analysis)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [query_trace.py](scripts/query_trace.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with shell commands and JSON-derived troubleshooting analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw SLS logs, ARMS spans, stack traces, source-code findings, and database troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
