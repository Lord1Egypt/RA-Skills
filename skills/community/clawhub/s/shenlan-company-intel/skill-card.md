## Description: <br>
当用户需要查询上市公司信息、追踪企业舆情、监控公告、按股票代码查找公司，或分析企业关联新闻时使用。通过深蓝财经API提供企业档案、舆情追踪、公告监控和热门企业排行。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenlannews](https://clawhub.ai/user/shenlannews) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business analysts use this skill to query public listed-company profiles, monitor announcements, track company mentions, and compare company attention signals through the Shenlan Finance API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public HTTPS requests to shenlannews.com for company, announcement, sentiment, and follower-attention data. <br>
Mitigation: Use it only when external API access to that provider is acceptable, and avoid sending private or sensitive company research unless the provider is trusted. <br>
Risk: Returned company intelligence can be mistaken for investment or financial advice. <br>
Mitigation: Treat outputs as informational business intelligence and verify material facts against official filings before making decisions. <br>


## Reference(s): <br>
- [深蓝企业情报 API 参考文档](references/api-reference.md) <br>
- [深蓝财经 Homepage](https://www.shenlannews.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/shenlannews/shenlan-company-intel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown summaries with JSON API results and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Public HTTPS requests to shenlannews.com; no credentials required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
