## Description: <br>
获取知乎每日热搜榜单，支持搜索、统计、范围分析。数据从 2021-01-08 至今。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doradx](https://clawhub.ai/user/doradx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Zhihu hot-search rankings, search current or historical entries, analyze date ranges, and export trend reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public data from GitHub-hosted sources, so results depend on network access and upstream data availability. <br>
Mitigation: Use it where outbound access to the public GitHub data source is acceptable, and treat unavailable or stale upstream data as an operational failure condition. <br>
Risk: Trend data is cached locally under ~/.cache/zhihu-hot. <br>
Mitigation: Use --no-cache for fresh reads or --clear-cache when cached trend data should not be retained. <br>
Risk: The --export option writes output to a user-supplied path. <br>
Mitigation: Review export destinations before running the command, especially in automated workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/doradx/zhihu-hot) <br>
- [Zhihu Hot Hub data source](https://github.com/SnailDev/zhihu-hot-hub) <br>
- [GitHub archives API used by the skill](https://api.github.com/repos/SnailDev/zhihu-hot-hub/git/trees/main?recursive=1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, files, guidance] <br>
**Output Format:** [Terminal text, Markdown reports, JSON objects, and exported files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports table, compact, single-line, JSON, search, date-range analysis, archive summary, cache statistics, and file export modes.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and script version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
