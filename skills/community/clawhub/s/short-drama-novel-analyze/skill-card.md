## Description:

把小说、连载网文或多集散稿拆成有据可查的原著拆解：支持全书或按创作者指定章节范围（如前 100 章、第一季）分批完成章节索引、改编价值快评、逐章情节提取、剧情单元与爽点梳理、人物与设定跨卷演进整理，给出结合目标制作形态的改编取舍建议与分集候选，移交 $short-drama-develop 定改编方案。用户说“导入这本小说”“拆这本书”“先拆前一百章”“分析原著”“这本书能不能改短剧”“把小说拆成分集候选”，或直接给出小说文件路径时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

创作者、编剧和开发团队可用此技能把拥有合法使用权的小说原文拆成可追溯的章节与剧情分析，并形成适配实拍或动态漫的改编建议和分集候选。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses file read and write capabilities, and one script was only partially inspected; runtime permission limits are unknown.

Mitigation: Review the scripts and limit filesystem access to the novel input and project output locations needed for the task.

Risk: Novel source text may be copyrighted or otherwise restricted.

Mitigation: Only process works the creator is entitled to use; keep source files read-only and avoid reproducing long passages in deliverables.

## Reference(s):

- [ClawHub release](https://clawhub.ai/worldwonderer/skills/short-drama-novel-analyze)
- [阶段规范](artifact/references/stage-contract.md)
- [改编价值快评](artifact/references/adaptation-triage.md)
- [逐章提取与人物设定整理](artifact/references/chapter-extraction.md)
- [改编价值与分集候选](artifact/references/adaptation-value.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, JSON Lines]

**Output Format:** [Markdown, JSON, and JSON Lines files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can cover the full work or a creator-specified chapter range; analysis records source chapter and line locations and avoids reproducing long passages.]

## Skill Version(s):

1.0.33 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
