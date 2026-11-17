## Description:

将 zread.ai 上指定仓库的既有 Wiki 完整导出为按章组织的本地 Markdown、索引和可续用的 Git 历史。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mc0571](https://clawhub.ai/user/mc0571)

### License/Terms of Use:

MIT-0

## Use Case:

开发者可用此技能保存并维护 Zread 仓库 Wiki 的完整原文，按章节生成 Markdown 与导航索引，并在后续续导时保留本地版本历史。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because it may modify its own instructions or maintenance source during a content export; the scan was partial and tool-misuse analysis was degraded for two scripts.

Mitigation: Review any skill-source changes and their diffs before accepting them or reusing the skill; treat the scan as incomplete.

## Reference(s):

- [Zread Wiki](https://zread.ai)
- [ClawHub skill release](https://clawhub.ai/mc0571/skills/zread-wiki-export)
- [Extraction methods and repair workflow](references/extraction.md)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [One Markdown file per Wiki chapter plus an index.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source language and records export progress; local Git history tracks changes.]

## Skill Version(s):

0.4.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
