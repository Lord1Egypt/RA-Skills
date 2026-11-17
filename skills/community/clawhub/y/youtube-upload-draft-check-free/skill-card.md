## Description:

使用用户明确指定的 Easy WebBridge browserId，只读核对本人 YouTube Studio 草稿或发布目标的可见字段并生成逐项来源及缺项清单；登录、所有权或目标不明确时停止，且不会发布或更改可见性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

面向需要发布前复核的 YouTube 创作者或运营人员，整理本人 Studio 草稿可见字段、缺项及来源，供人工检查与交接。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conflicting browser-selection instructions could expose private drafts through an unintended session.

Mitigation: Resolve the conflict so every read uses the user's explicitly selected browserId; stop if login, ownership, or draft selection is unclear.

Risk: Unrelated promotional directions are included with the review workflow.

Mitigation: Remove the promotional directions before use.

Risk: Offline fixtures do not verify the user's live YouTube account.

Mitigation: Treat offline results as checks of local checklist logic only; verify live visible fields and their sources in the selected account.

## Reference(s):

- [EasyBR AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)
- [EasyBR 下载页](https://www.ebrower.com/down.html)
- [Easy WebBridge 技术参考](https://github.com/aiispower/easy-webbridge)
- [Easy WebBridge Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown checklist with visible field values, missing items, and per-item sources]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only checklist for a single draft or publishing target.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
