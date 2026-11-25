## Description:

将已生成的短剧镜头与配音剪成成片，编写剪辑单并完成渲染验收。用于“剪成成片/套剪”“加字幕/画面文字”“统一响度”“调整成片剪辑节奏、配乐/字幕混音与渲染导出”或导出精修素材；需补素材或改故事时转回上游阶段。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT-0

## Use Case:

短剧创作者和剪辑人员可用此技能依据已有镜头与配音编写剪辑单、安排镜序和字幕，并渲染及验收短剧成片。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 安全扫描报告了路径重定向导致写入预期输出目录以外位置的风险，且扫描未完成。

Mitigation: 安装前检查技能权限和输出路径；仅在意外文件修改范围受限的环境中使用，并结合不完整扫描审查技能。

## Reference(s):

- [剪辑单格式规范](references/format-spec.md)
- [短剧剪辑实务指南](references/editing-guide.md)
- [阶段职责与规则](references/stage-contract.md)
- [Remotion 图文叠加层说明](assets/remotion/README.md)
- [ClawHub 技能页面](https://clawhub.ai/worldwonderer/skills/short-drama-edit)

## Skill Output:

**Output Type(s):** [Markdown, Video, Shell commands]

**Output Format:** [Markdown 剪辑单与渲染后的成片视频]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [可选输出字幕、图文叠加层及分段中间文件。]

## Skill Version(s):

1.0.25 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
