## Description:

为中文自媒体创作者和小店经营者把 AI 视频画面意图与原始提示词整理为可复制的最终提示词、镜头动作顺序和连续性约束；不调用视频生成 API，不捏造视频模型参数，并明确区分提示词写作模型与实际生成模型。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

中文内容创作者和小店经营者可用此技能，把视频画面意图与草稿提示词整理成可交给视频生成工具的中文提示词、镜头动作顺序、连续性约束及与原稿的对比说明。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 安装命令未固定 `skills` CLI 版本，安装时可能运行后续版本并使用账户权限。

Mitigation: 安装前检查命令解析出的包；如继续安装，使用不含敏感凭据的环境。

Risk: 扫描仅部分检查了一个被引用脚本，且未覆盖二进制素材。

Mitigation: 安装前检查相关脚本与素材，并在部署前完成技能审查和扫描。

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [四个部分：最终提示词、镜头动作顺序、连续性约束、对比与待确认；不生成视频。]

## Skill Version(s):

1.0.2 (source: package.json, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
