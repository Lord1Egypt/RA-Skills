## Description: <br>
公众号搜索工具，支持按关键词搜索爆款文章，展示推荐热门文章，助力内容创作者把握趋势与获取灵感。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, new media operators, and self-media teams use this skill to search recent WeChat public-account articles, compare popularity and relevance signals, and find topic inspiration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation includes an apparent API key and the skill requires a RedFox API key. <br>
Mitigation: Do not reuse embedded credentials; configure only your own REDFOX_API_KEY after deciding you trust RedFox with submitted keywords and date ranges. <br>
Risk: The subscription workflow can create persistent calendar or reminder entries, with incomplete cancellation and privacy detail in the evidence. <br>
Mitigation: Confirm how subscription reminders are stored, delivered, and cancelled before enabling daily pushes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/wechat-explosive-content) <br>
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [WeChat trend data format reference](references/gzh_trend_data_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown tables and prompts, JSON script output, and optional HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may create calendar/reminder subscriptions when the user opts in.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
