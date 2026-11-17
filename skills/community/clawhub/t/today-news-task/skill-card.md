## Description:

抓取国内门户页面并汇总热点资讯。Use When 需要国内外热点与科技数码的要闻摘录。且可选择是否将结果推送到负一屏。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzh2607](https://clawhub.ai/user/lzh2607)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect current headlines from major Chinese news and technology portals, filter duplicate or low-quality items, and produce a categorized Markdown news brief. Users may optionally pass the completed brief to a separate today-task skill for task-screen publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow runs a local Python URL-fetching script that can request arbitrary URLs.

Mitigation: Keep use limited to the listed public news and search pages, and avoid private-network, localhost, file, metadata-service, or untrusted redirected URLs.

Risk: The optional push workflow depends on a separate unpinned today-task skill.

Mitigation: Review and install today-task from a trusted ClawHub source before using the optional publishing step.

## Reference(s):

- [Today News Task on ClawHub](https://clawhub.ai/lzh2607/skills/today-news-task)
- [today-task skill](https://clawhub.ai/skills/today-task)
- [today-task skill on ClawHub China mirror](https://cn.clawhub-mirror.com/skills/today-task)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown news brief with source links and optional task payload guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Categorizes items into domestic, international, and technology sections; optional push workflow uses fields required by today-task.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
