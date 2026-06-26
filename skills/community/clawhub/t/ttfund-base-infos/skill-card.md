## Description: <br>
通过天天基金 API 查询指定基金代码的基金基础信息，包括基金名称、类型、基金公司、当前净值和风险等级等核心数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yemeng831-cloud](https://clawhub.ai/user/yemeng831-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch and summarize 天天基金 fund base information for a supplied fund code. It guides API-key setup, constructs the request, and explains returned fields for user-facing fund information lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The user's 天天基金 API key is sent to the skill gateway when fund information is requested. <br>
Mitigation: Store the key in TTFUND_APIKEY, use a dedicated or limited-scope key if available, and avoid sharing the key in prompts or logs. <br>
Risk: Returned fund information could be mistaken for investment advice. <br>
Mitigation: Treat results as informational data for the current lookup and verify important details before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yemeng831-cloud/ttfund-base-infos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with JSON business data and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TTFUND_APIKEY and a fund code; returned fund data should be treated as informational, not investment advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
