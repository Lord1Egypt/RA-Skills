## Description: <br>
股票机构消息日报筛选工具，从指定 API 信源获取当日机构研报和资讯，按影响力、重要性、新颖性等维度筛选并输出 Top 20 精选日报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raisonliu](https://clawhub.ai/user/raisonliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and agents use this skill to fetch the current day's A-share institutional market messages, rank the most important items, and produce a concise daily digest. The output is intended as a market-news summary and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill summarizes an unverified external market-news feed that may contain inaccurate, incomplete, or time-sensitive investment information. <br>
Mitigation: Treat the result as a news digest rather than investment advice, and confirm important market or company claims with trusted sources before acting. <br>
Risk: The skill contacts a disclosed external HTTP API. <br>
Mitigation: Review the endpoint and network policy before use in restricted environments. <br>


## Reference(s): <br>
- [A股当日机构消息 ClawHub page](https://clawhub.ai/raisonliu/xxjhe-ashare-daily-info) <br>
- [Daily institutional message API feed](http://81.68.131.238/api/today) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, API Calls] <br>
**Output Format:** [Markdown daily digest] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Top 20 ranked items plus a one-sentence core theme, based only on fetched feed content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
