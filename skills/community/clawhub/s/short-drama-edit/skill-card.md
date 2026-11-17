## Description:

将已生成的短剧镜头剪成成片，记录入出点、镜序、声音、字幕与交付规格。用于套剪、加字幕、统一响度、调整节奏或导出精修素材；需要补素材或修改故事时转回对应创作阶段。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

短剧创作者和剪辑人员可用此技能依据分镜与剧本整理逐镜素材，设置切点、声音和字幕，并检查、导出成片。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this skill suspicious for substantial resource and file-write risks; only part of the artifact was fully scanned, so the scan cannot establish that it is safe.

Mitigation: Before use, review media-processing limits and output-write destinations, restrict runs to intended project and output directories, and try bounded inputs on copies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/worldwonderer/skills/short-drama-edit)
- [短剧剪辑实务指南](references/editing-guide.md)
- [剪辑阶段职责与规则](references/stage-contract.md)
- [Remotion 图文叠加层说明](assets/remotion/README.md)
- [Remotion license terms](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Video files]

**Output Format:** [Markdown 剪辑单、用于检查与渲染的 shell 命令，以及渲染后的 MP4 成片]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [剪辑单记录分段、时间点、声音、字幕和交付规格；成片规格由剪辑单设定。]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
