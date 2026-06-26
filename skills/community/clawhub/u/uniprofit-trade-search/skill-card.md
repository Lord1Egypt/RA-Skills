## Description: <br>
Searches UniProfit trade intelligence data through the OpenClaw-compatible UniProfit API for importer lookup, exhibition lead search, and purchase requirement search with a user-created trade_search API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xieziqing](https://clawhub.ai/user/xieziqing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan and execute scoped UniProfit trade-data searches for buyer or importer leads, exhibition contacts, and procurement demand, then summarize actionable result windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a scoped UniProfit API key and search filters to the configured UniProfit API. <br>
Mitigation: Confirm UNIPROFIT_API_BASE_URL points to the legitimate UniProfit service, use a scoped trade_search key, and rotate the key if it is exposed. <br>
Risk: Search filters may reveal confidential business strategy or unnecessary personal data. <br>
Mitigation: Avoid putting confidential strategy or unnecessary personal data in filters, and review planned queries before execution. <br>
Risk: Unsupported or overly broad filters can fail or spend limited search quota without useful results. <br>
Mitigation: Use the supported filters for the chosen source, ask one clarifying question when the plan is weak, and narrow filters before retrying or paging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xieziqing/uniprofit-trade-search) <br>
- [API Reference](references/api.md) <br>
- [Query Patterns](references/query-patterns.md) <br>
- [Error Handling](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands and structured result details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a scoped UniProfit trade_search API key and summarizes current result windows rather than full database counts.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
