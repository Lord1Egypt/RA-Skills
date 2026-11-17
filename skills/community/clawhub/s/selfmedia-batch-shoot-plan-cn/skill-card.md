## Description:

输入已经定稿的多条短视频脚本、人物、场地和道具信息，输出按场景与机位合并的拍摄顺序、现场核对项和素材命名表，适合单次章节、场景或短文的集中拍摄。仅整理用户材料，不改写小说或生成分镜；缺少脚本编号、场景、人物或动作摘要时先列缺项；场地映射、机位或拍摄时段未给时标待确认。单表最多100行，超出时要求分批提交。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

适合自媒体创作者和现场制作人员整理已定稿的短视频脚本，按场景与机位安排拍摄顺序并生成素材命名表；资料不全时先列缺项，不补写剧情或分镜。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 用户可能在脚本或制作资料中提供不必要的敏感信息。

Mitigation: 仅提供完成拍摄计划所需的制作信息；无需提供账户凭据。

Risk: 缺少布置、排练、拍摄或重拍耗时可能导致错误的钟点排期。

Mitigation: 确认缺失的现场耗时后再制定钟点安排；信息不足时只给非钟点顺序。

## Reference(s):

- [ClawHub release](https://clawhub.ai/xxjrq/skills/selfmedia-batch-shoot-plan-cn)
- [Project repository (listed in manifest)](https://github.com/xxjrq/selfmedia-batch-shoot-plan-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown tables for the shoot order and media naming plan, or a missing-information list when core details are absent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 100 script or scene records per batch; omits clock times when production durations or availability are unknown.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
