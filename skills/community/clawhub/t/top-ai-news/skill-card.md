## Description: <br>
获取 AI 每日新闻 TOP 10，包含日期标题和新闻标题，格式简洁. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajian11](https://clawhub.ai/user/ajian11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch the latest AI news headlines from a public daily AI news page and return a concise top 10 list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on ai-bot.cn availability and the current page content. <br>
Mitigation: Treat returned headlines as public web content and retry or review the source page if results appear incomplete or stale. <br>
Risk: The skill opens an external public website in a browser. <br>
Mitigation: Use it only when browser access to ai-bot.cn is acceptable; the evidence reports no credential, local-file, persistence, or mutation behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ajian11/top-ai-news) <br>
- [Publisher profile](https://clawhub.ai/user/ajian11) <br>
- [AI daily news source](https://ai-bot.cn/daily-ai-news/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown numbered list with a current-date heading] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to ten ranked AI news headlines, continuing across date sections if needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
