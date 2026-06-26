## Description: <br>
获取并整理多平台实时热点新闻，按跨平台热度共识筛选，输出高热度事件的简报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerry48](https://clawhub.ai/user/jerry48) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who monitor Chinese-language public trends use this skill to collect hot-list entries from multiple public platforms, cluster cross-platform topics, and produce a short Markdown brief for Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated hot-news brief is sent to a Feishu channel and may reach an unintended workspace audience. <br>
Mitigation: Confirm the destination Feishu channel is appropriate before running the skill. <br>
Risk: The skill fetches public trending pages and sends an outbound message, which may be restricted in some environments. <br>
Mitigation: Run it only where scraping public trending pages and sending outbound Feishu messages are permitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerry48/realtime-hot) <br>
- [Weibo trending source](https://rebang.today/?tab=weibo) <br>
- [Douyin trending source](https://rebang.today/?tab=douyin) <br>
- [Toutiao trending source](https://rebang.today/?tab=toutiao) <br>
- [Baidu trending source](https://rebang.today/?tab=baidu) <br>
- [Zhihu trending source](https://rebang.today/?tab=zhihu) <br>
- [Tencent trending source](https://tophub.today/n/qndg48xeLl) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text] <br>
**Output Format:** [Markdown brief] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The fetch step writes scripts/hot-data.json, and the formatter emits the final brief to stdout for Feishu delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
