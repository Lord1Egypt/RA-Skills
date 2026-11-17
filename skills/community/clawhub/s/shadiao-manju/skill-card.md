## Description:

把一句话、小说或热点编排为 1–2 分钟竖屏搞笑动画，涵盖剧本、配音、素材、工程生成、导出和质检。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongzichixiangjiao](https://clawhub.ai/user/kongzichixiangjiao)

### License/Terms of Use:

MIT No Attribution

## Use Case:

创作者和内容团队可用它把一句话、小说或热点制作为 1–2 分钟竖屏搞笑动画，并完成从剧本到上线质检的制作流程。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 精心构造的项目元数据可能导致素材索引覆盖项目目录外的图片。

Mitigation: 使用可信且自行生成的项目元数据，先校验目标文件名和完整路径，并限制进程可访问的文件系统范围。

Risk: 云端语音合成会把台词发送给 Microsoft，AI 生图会把提示词和参考图发送给火山方舟。

Mitigation: 处理未公开或敏感内容前先确认允许外发；不允许外发时使用本地语音引擎，并跳过云端生图。

Risk: 外部动画应用及可选音色克隆工具链尚未经过此版本的审计。

Mitigation: 安装前审查并固定外部应用及依赖版本；启用克隆前确认已获得声音权利人授权。

## Reference(s):

- [项目主页](https://github.com/kongzichixiangjiao/shadiao-manju)
- [沙雕动画小助手 Web 社区版](https://github.com/wormsun/FunnyAnimationAssitant)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration, Audio, Images, Video]

**Output Format:** [Markdown、JSON、音频与图像素材、.anime 工程文件和 MP4 视频]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [面向 1–2 分钟竖屏喜剧短片；预览和最终导出需在浏览器中人工完成。]

## Skill Version(s):

1.0.5 (source: changelog, released 2026-11-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
