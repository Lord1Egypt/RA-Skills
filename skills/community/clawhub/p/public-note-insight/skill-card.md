## Description:

查询小红书公开笔记、评论和博主内容，为内容研究与趋势分析提供结构化数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

面向小红书创作者、运营和市场研究人员，按关键词查找公开笔记，查看笔记详情、评论和博主公开作品。可将返回的数据用于选题调研、竞品观察和评论观点归纳。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Xiaohongshu links are sent to the Guaikei data service.

Mitigation: Use only non-sensitive query terms and links to public content.

Risk: Successful results are saved under the system temporary directory.

Mitigation: Set XHS_GUAIKEI_DISABLE_LOG=1 to disable local result logging, and avoid queries involving sensitive information.

Risk: The listing mentions multiple social platforms, while the artifact documents Xiaohongshu only.

Mitigation: Treat this release as Xiaohongshu-only and confirm platform coverage before cross-platform research.

## Reference(s):

- [Guaikei data service](https://www.guaikei.com)
- [Command options](references/options.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON response envelope containing public Xiaohongshu search, post, comment, or creator data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interaction counts are returned as strings; results can support follow-up summaries and research.]

## Skill Version(s):

1.2.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
