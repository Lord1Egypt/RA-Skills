## Description: <br>
招投标快捷检索引擎-标找找，当用户需要快速查询特定关键词的招标或中标公告时调用，优先调用基础搜索工具提取项目名称、金额和链接，输出精简直接的列表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and procurement teams use this skill to search tender and award notices, retrieve bid details, analyze companies, compare suppliers, and summarize procurement market signals from the Biaozhaozhao API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is described as a quick tender search tool while enabling broader procurement intelligence, contact lookup, and web-enhanced research. <br>
Mitigation: Install only when those broader procurement-intelligence capabilities are expected, and scope use to legitimate business research. <br>
Risk: Search terms, company names, and related queries may be sent to the Biaozhaozhao API and sometimes to web search during analysis features. <br>
Mitigation: Avoid entering confidential strategy, regulated personal data, or sensitive customer information unless disclosure to those services is approved. <br>
Risk: Returned contact details can include sensitive business or personal data. <br>
Mitigation: Use contact information only for authorized procurement workflows; avoid bulk harvesting, unsolicited outreach, or retention beyond business need. <br>


## Reference(s): <br>
- [Biaozhaozhao API documentation](https://ai.zhiliaobiaoxun.com/docs/api/) <br>
- [Biaozhaozhao API access portal](https://ai.zhiliaobiaoxun.com) <br>
- [ClawHub skill release page](https://clawhub.ai/liu-jiapeng/tender-search-biaozhaozhao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown summaries with structured lists and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY for authenticated Biaozhaozhao API access.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
