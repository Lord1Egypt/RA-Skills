## Description:

搜索 TikTok 公开关键词结果、博主作品和视频评论，并以 JSON 返回，供趋势、竞品和舆情分析使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

创作者、品牌和 MCN 团队可用此技能检索 TikTok 公开视频、博主作品和评论，为选题发现、竞品跟踪及舆情分析获取数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and TikTok targets are sent to Guaikei, and API use may incur charges.

Mitigation: Review Guaikei privacy terms and current pricing before use; keep result limits appropriate.

Risk: Results can include public usernames and comment content that may need care when shared.

Mitigation: Confirm authorization before external or commercial publication and redact usernames where appropriate.

Risk: Optional logging can retain result data in local temporary storage.

Mitigation: Leave optional logging disabled unless needed, and handle any saved results according to your data policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/tiktok-videos-search)
- [Guaikei service](https://www.guaikei.com)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Structured data]

**Output Format:** [JSON envelope containing video search results, creator posts, or video comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results distinguish empty responses from errors; timestamps use Beijing time.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter, changelog dated 2026-11-04, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
