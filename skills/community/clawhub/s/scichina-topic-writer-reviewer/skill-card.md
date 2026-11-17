## Description:

科普智创审校助手帮助代理采集科普中国热点内容，提炼主题关键词，撰写科普文章，并执行科学性、引用来源和事实核查审校。

This skill is ready for commercial/non-commercial use.

## Publisher:

[binhuatochina](https://clawhub.ai/user/binhuatochina)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and science communication teams use this skill to turn current KepuChina topics into public-facing science articles with source checks and an audit-style review report before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish generated content to a fixed Feishu location, grant edit access, and store document links locally without clear user approval.

Mitigation: Review before installing and require explicit confirmation of the destination workspace, document permissions, and external write action before any Feishu document is created or shared.

Risk: Science or medical content may contain unsupported claims if source verification is skipped or incomplete.

Mitigation: Use the built-in scientific, citation, and fact-check review steps, mark unverifiable references as pending verification, and avoid publishing until authoritative sources support the claims.

## Reference(s):

- [科普中国](https://www.kepuchina.cn/)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration]

**Output Format:** [Markdown articles, reference lists, review reports, Feishu document content, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Feishu documents, grant edit access, and save document links locally when the configured tools are available.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
