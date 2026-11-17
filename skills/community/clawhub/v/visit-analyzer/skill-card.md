## Description:

拜访记录分析引擎。根据员工的拜访沟通记录，AI 分析销售阶段、跟进策略、客户洞察、承诺事项和风险预估。当员工要求查看某个客户/公司的聊天分析时触发，自动生成项目画像并输出 H5 链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

Sales employees use this skill to analyze visit records, phone transcripts, and WeChat chat records for a customer or project. It produces sales-stage assessment, follow-up strategy, customer insights, commitments, risk estimates, and a project-portrait link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account passwords, bearer tokens, and private visit or chat communications.

Mitigation: Require review before installation, avoid password entry in chat, store credentials in a secure credential store, and obtain explicit confirmation before reading or uploading communications.

Risk: The security guidance says network traffic and the project-portrait link should not rely on HTTP or bearer-token URL fallback.

Mitigation: Replace HTTP endpoints with HTTPS on a verified domain and remove token-bearing URL fallback before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/visit-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with structured analysis fields and an H5 project-portrait link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and python3 on Linux or macOS; analysis is expected to be based on actual visit or chat records.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
