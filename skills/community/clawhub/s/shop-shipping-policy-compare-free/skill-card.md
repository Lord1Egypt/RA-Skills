## Description:

在用户指定的 Easy WebBridge 浏览器环境中，只读核对 2–3 个公开配送或售后政策页并整理可追溯对照表，列出发货时效、适用地区、费用条件及缺项，对归属不明、冲突或不完整的信息明确标注且不推断运费、送达或交易结论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

外部用户、店铺运营人员和客服人员可用此技能核对 2–3 个公开配送或售后政策页，整理发货时效、适用地区、费用条件及缺失或冲突条款，并保留页面来源。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 浏览器配置选错或意外启用草稿填写，可能影响非目标账号或页面内容。

Mitigation: 使用专用浏览器配置并明确选择 browserId；除非用户授权，否则保持草稿填写关闭，且绝不发布或发送。

Risk: 为设置浏览器连接而下载的软件或依赖，其安全性未由随附技能文件证实。

Mitigation: 安装前核对安装包来源和依赖版本。

## Reference(s):

- [Easy WebBridge (GitHub)](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge 镜像 (Gitee)](https://gitee.com/xxjrq/easy-webbridge)
- [EasyBR 下载页](https://www.ebrower.com/down.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown 对照表，附来源 URL 与缺失项清单]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [最多 100 行；只报告页面可见内容，不推断运费或送达承诺。]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
