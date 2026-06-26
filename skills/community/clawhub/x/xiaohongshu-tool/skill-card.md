## Description: <br>
小红书运营数据工具，用于关键词搜索、笔记详情与评论分析、博主作品监控、爆款挖掘、竞品分析、KOL筛选和趋势洞察。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[um-why](https://clawhub.ai/user/um-why) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, brand marketers, market analysts, MCN teams, and agents use this skill to query public Xiaohongshu data, inspect notes and comments, monitor creator posts, and prepare competitive or trend analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Xiaohongshu keywords, note URLs, profile URLs, and GUAIKEI_API_TOKEN to a third-party API service. <br>
Mitigation: Use only approved tokens and non-sensitive research terms, and confirm the API service is acceptable for the intended workspace before running commands. <br>
Risk: Fetched results are automatically written to local JSON files under the skill's logs directory. <br>
Mitigation: Run on trusted machines, review log contents after use, and delete logs that contain sensitive research terms or business analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/um-why/xiaohongshu-tool) <br>
- [完整选项说明](references/options.md) <br>
- [技能更新日志](references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON data, shell commands, configuration guidance] <br>
**Output Format:** [CLI stdout in JSON or Markdown, with results also saved as local JSON log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; commands accept keyword, Xiaohongshu note/profile URL, sorting, time, limit, and output-format options.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata, SKILL.md frontmatter, package.json, references/changelog.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
