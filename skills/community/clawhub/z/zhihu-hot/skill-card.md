## Description:

获取知乎每日热搜榜单，支持搜索、统计、范围分析。数据从 2021-01-08 至今。

This skill is ready for commercial/non-commercial use.

## Publisher:

[doradx](https://clawhub.ai/user/doradx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve, search, export, and analyze Zhihu hot-search archive data from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI fetches public archive data from GitHub-hosted Zhihu data and displays it in terminal, Markdown, or JSON output.

Mitigation: Treat fetched content as untrusted and review terminal or Markdown output before forwarding, publishing, or automating it.

Risk: Export mode writes to a user-provided path and can overwrite an existing file.

Mitigation: Use deliberate export paths and review destination files before running scheduled or automated exports.

Risk: The skill stores cache files under ~/.cache/zhihu-hot.

Mitigation: Use --clear-cache when cached data should be removed, and inspect cache behavior before deployment in constrained environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/doradx/skills/zhihu-hot)
- [zhihu-hot-hub data source](https://github.com/SnailDev/zhihu-hot-hub)
- [GitHub tree API used for archive discovery](https://api.github.com/repos/SnailDev/zhihu-hot-hub/git/trees/main?recursive=1)
- [Raw GitHub content base used by the CLI](https://raw.githubusercontent.com/SnailDev/zhihu-hot-hub/main)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Analysis]

**Output Format:** [Terminal text, Markdown reports, JSON objects, or exported files depending on CLI flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache fetched archive data under ~/.cache/zhihu-hot and may overwrite user-selected export files.]

## Skill Version(s):

3.0.0 (source: release evidence and script __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
