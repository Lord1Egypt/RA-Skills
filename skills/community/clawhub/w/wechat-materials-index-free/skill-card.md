## Description:

在用户指定的 Easy WebBridge 浏览器会话中，只读整理本人公众号素材库当前可见内容：按主题筛选并最多提取20条名称、类型、可见日期与使用待办，交付带逐条页面来源和缺项说明的 Markdown 草稿。适用于一次性盘点已授权页面；登录、验证码、风控、权限不足或所有权不明时停止，历史内容未显示时作为缺项保留，不把可见清单说成完整历史盘点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

公众号运营者和内容团队可用此技能整理本人素材库中当前可见的素材，按主题生成带逐条页面来源、缺项和范围说明的 Markdown 目录草稿。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security guidance flags an unpinned installer as a consideration.

Mitigation: Verify the download source and select a specific release before installing browser tooling.

Risk: The security summary reports a mismatch between the declared read-only purpose and scanner-reported installation and extra capabilities; analysis was partial.

Mitigation: Review the requested browser access and keep collection within the user-selected environment; stop on login, CAPTCHA, risk-control, permission, or ownership uncertainty. Review any partly inspected or out-of-scope content before deployment.

## Reference(s):

- [EasyBR official download page](https://www.ebrower.com/down.html)
- [EasyBR v1.7.8 release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)
- [Easy WebBridge (GitHub)](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge (Gitee mirror)](https://gitee.com/xxjrq/easy-webbridge)
- [ClawHub skill page](https://clawhub.ai/xxjrq/skills/wechat-materials-index-free)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown directory draft with a table of visible materials, per-item sources, gaps, and a scope statement]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 20 currently visible items; records missing or unavailable information and does not claim a complete historical inventory.]

## Skill Version(s):

1.0.1 (source: manifest.yaml, SOURCE-ORIGIN.md, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
