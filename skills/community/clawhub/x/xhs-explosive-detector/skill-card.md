## Description: <br>
小红书热门笔记搜索工具，支持关键词搜索获取热门内容数据，基于数据评分排序推荐热门笔记，助力创作者发现热门趋势、获取创作灵感。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, brands, MCNs, and content operators use this skill to search Xiaohongshu trending notes by keyword and date range, compare scored examples, and generate a local report for topic planning or competitor review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Redfox API key and uses it to request Xiaohongshu search data. <br>
Mitigation: Keep REDFOX_API_KEY in environment or secret configuration, and avoid exposing it in code, prompts, screenshots, logs, or output files. <br>
Risk: Search terms and date ranges are shared with Redfox, and the skill stores generated HTML reports in the local working directory. <br>
Mitigation: Install only when that data sharing and local report storage are acceptable for the intended use case. <br>
Risk: The skill can optionally create a recurring calendar subscription for the current search. <br>
Mitigation: Confirm the subscription option only when recurring reminders tied to the current search are desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/xhs-explosive-detector) <br>
- [Xiaohongshu hot article data format](references/xhs_hot_article_format.md) <br>
- [Redfox Hub API keys](https://redfox.hk/dashboard/keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, HTML, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown tables and prompts, with a local HTML report file and optional shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; may create a calendar subscription only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
