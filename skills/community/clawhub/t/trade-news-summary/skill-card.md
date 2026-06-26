## Description: <br>
Aggregates trade-related RSS news, translates news titles into Chinese, writes a Markdown report, and can push generated updates to a configured Feishu chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joewangup](https://clawhub.ai/user/joewangup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business operators use this skill to collect trade-related public news, translate titles for Chinese-language review, generate a daily Markdown briefing, and optionally post summary cards to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News titles are sent to Baidu Translate during report generation. <br>
Mitigation: Use the skill only with public RSS sources or non-sensitive keywords, and use dedicated Baidu API credentials. <br>
Risk: Generated reports can be posted to the configured Feishu chat. <br>
Mitigation: Use a dedicated Feishu webhook and confirm the target chat before enabling FEISHU_WEBHOOK. <br>
Risk: Reports and trend history may remain on disk after execution. <br>
Mitigation: Remove ~/trade-news.md and ~/.openclaw/workspace/history when retained report or trend data is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joewangup/trade-news-summary) <br>
- [Baidu Translate Open Platform](https://fanyi-api.baidu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report and Feishu interactive message payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes ~/trade-news.md and may retain trend history under ~/.openclaw/workspace/history.] <br>

## Skill Version(s): <br>
2.3.3 (source: server release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
