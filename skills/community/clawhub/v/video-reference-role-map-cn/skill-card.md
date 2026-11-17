## Description:

将用户授权的参考素材清单与视频生成目标整理为可执行分工表，逐项标明身份、地点、风格和动作用途，并提示冲突与缺料。适用于单章节、单场景或短文的视频参考梳理；最多处理100行，超量时要求分批，不下载外部来源也不虚构模型参数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

面向视频创作者与制作人员，帮助将用户授权的参考素材映射到身份、地点、风格和动作职责，并指出冲突与必需补料。仅依据本轮提供的信息整理，不下载外部素材或推测模型参数。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 未获授权的参考素材可能被用于分工。

Mitigation: 仅提供获授权使用的素材，并遵守各项素材的允许用途。

Risk: 素材描述不足可能导致职责判断不确定。

Mitigation: 将无法确认的栏位标为待确认，并补充可见内容或必要的动作时序信息。

Risk: 通过 README 安装时可能选择未经核验的发布者或版本。

Mitigation: 安装前核验发布者，并优先使用已审阅且固定版本的发布包。

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xxjrq/skills/video-reference-role-map-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown表格，列出各参考素材的身份、地点、风格和动作用途及冲突说明，并附缺项与下一步]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [每次最多处理100项；更多素材需按章节、场景或批次拆分。]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
