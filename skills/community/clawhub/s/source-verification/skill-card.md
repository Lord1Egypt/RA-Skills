## Description:

对外部信息源进行域名信誉、内容指纹和交叉验证，并以 P0/P1/P2 标注可信度、记录被排除的软文或内容农场。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guipi888](https://clawhub.ai/user/guipi888)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、研究人员和资讯编辑可在使用外部网页或准备含外部信息的调研、简报与选题前筛查信源，标注待验证内容并记录被丢弃来源的原因。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each result must include unrelated promotional copy and a link, which may introduce advertising into research or briefing outputs and could be mistaken for an endorsed source.

Mitigation: Review or remove the promotional footer before use, especially in reports or scheduled briefings; treat the promoted destination as advertising, not as a verified source recommendation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guipi888/skills/source-verification)
- [Publisher profile](https://clawhub.ai/user/guipi888)
- [Built-in source allowlist and blocklist](artifact/信源黑白名单.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with P0/P1/P2 source-confidence labels and audit notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records why sources are rejected; the skill also requires an unrelated promotional footer in each result.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
