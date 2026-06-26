## Description: <br>
获取今日最热门的科技资讯，特别是 AI 大模型领域的最新动态。支持多数据源自动切换（Tavily API→科技网站直连），适合每日科技简报、行业资讯收集、AI 领域跟踪等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchaoqun](https://clawhub.ai/user/chenchaoqun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to collect a daily Chinese technology-news brief, with emphasis on AI and large-model developments, from Tavily or fallback technology sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to search services or technology-news websites, and a configured Tavily API key may incur account-linked quota usage. <br>
Mitigation: Use it only when external technology-news retrieval is intended, scope the Tavily key appropriately, and monitor quota or account usage. <br>
Risk: Recurring cron usage can trigger daily outbound requests without a fresh manual prompt. <br>
Mitigation: Enable scheduled runs only deliberately, and review the schedule, time zone, and destination before deployment. <br>
Risk: News summaries can inherit stale, duplicated, or inaccurate information from upstream sources. <br>
Mitigation: Review the linked source articles before relying on the briefing for decisions. <br>


## Reference(s): <br>
- [Search Queries Reference](references/search-queries.md) <br>
- [Tavily Documentation](https://docs.tavily.com/) <br>
- [Tavily](https://tavily.com/) <br>
- [36Kr AI Channel](https://36kr.com/motifs/806919956817) <br>
- [机器之心](https://www.jiqizhixin.com/) <br>
- [量子位](https://www.qbitai.com/) <br>
- [AI 科技大本营](https://aitechtalk.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/chenchaoqun/tech-news-daily) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown news briefing with titles, summaries, timestamps, and source links; helper scripts may emit JSON search instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Top 10 items by default; may use Tavily API or direct technology-site fetches.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
