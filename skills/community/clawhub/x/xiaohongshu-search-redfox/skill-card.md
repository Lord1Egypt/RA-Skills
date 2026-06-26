## Description: <br>
小红书热门笔记搜索工具，支持关键词搜索、数据评分排序、趋势推荐和本地 HTML 报告生成，帮助创作者、品牌方和 MCN 机构发现热门内容趋势。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, brand teams, MCNs, and content operations teams use this skill to search Xiaohongshu trending notes by keyword and time window, compare engagement and scoring signals, generate local HTML reports, and optionally set recurring trend subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Redfox API key. <br>
Mitigation: Store REDFOX_API_KEY only in approved environment configuration, confirm the key scope and revocation path, and avoid hard-coding or exposing it in prompts, logs, or output files. <br>
Risk: Search terms and date filters are sent to redfox.hk. <br>
Mitigation: Avoid confidential or sensitive search terms unless sharing them with the Redfox service is approved for the user's environment. <br>
Risk: The skill can create local HTML report files in the working directory. <br>
Mitigation: Review output paths and handle generated reports as local artifacts that may contain external links and trend data. <br>
Risk: Calendar subscriptions can create recurring reminder behavior. <br>
Mitigation: Use subscriptions only when the user explicitly wants recurring trend updates, and review how to disable or remove the subscription. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/xiaohongshu-search-redfox) <br>
- [Redfox Hub API keys](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [Xiaohongshu hot article format](references/xhs_hot_article_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, HTML files, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with ranked note tables, JSON from the Python script, and keyword-named local HTML report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; search terms and date filters are sent to redfox.hk, and HTML reports may be written in the working directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
