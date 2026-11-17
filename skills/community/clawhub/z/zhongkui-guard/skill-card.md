## Description:

检查指定的 AI Skill、模型响应和工具调用中的可疑指令，脱敏本地文件，并对用户指定的模型 API 做能力体检。适用于中转站投毒风险排查、资料发送前脱敏和模型质量对照；使用本地脚本生成证据，不提供全局自动拦截或模型真伪认证。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill to scan selected skill files, model responses, and tool logs for suspicious instructions, create redacted local copies before sharing content, and run user-confirmed model API capability checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan and audit results may be mistaken for proof that a file, skill, response, or model is safe.

Mitigation: Treat findings as review leads, and explain coverage and limitations with every report.

Risk: Endpoint capability checks can use API credentials and send requests to a configured model endpoint.

Mitigation: Run audit planning first, confirm the target endpoint, budget, TLS behavior, and credentials, and provide credentials only for trusted endpoints.

Risk: Redaction covers selected text-oriented formats and may not remove every kind of sensitive information.

Mitigation: Use explicit input and output paths, review the generated copy before sharing, and do not treat unsupported file types or semantic secrets as covered.

## Reference(s):

- [钟馗卫士 ClawHub listing](https://clawhub.ai/dongsheng123132/skills/zhongkui-guard)
- [扫描](references/scan.md)
- [脱敏](references/privacy.md)
- [模型体检](references/audit.md)
- [兼容性](references/compatibility.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON results, Markdown reports, shell commands, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local operations use explicit input and output paths; endpoint audits require user-confirmed configuration and credentials.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
