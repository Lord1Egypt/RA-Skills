## Description:

根据公司名称查询企业基本信息、知识产权（专利/商标/著作权），数据来源企查查、天眼查等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigxiaoxin](https://clawhub.ai/user/bigxiaoxin)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to look up public Chinese company information and intellectual-property summaries by company name, then review source links for fuller records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names and related investigative interests are sent to Tavily, which is not disclosed in the skill documentation.

Mitigation: Disclose Tavily as a lookup service and avoid sensitive searches until that data flow is acceptable to the user or organization.

Risk: The skill contains an embedded Tavily API key.

Mitigation: Remove the embedded key, rotate it, and require users to provide their own credential through a runtime secret or environment variable.

Risk: The security guidance calls out an unused dependency and HTTP package sources.

Mitigation: Remove unused dependencies and use HTTPS package sources before treating the skill as a normal low-risk lookup skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigxiaoxin/skills/qichacha)
- [Qichacha search](https://www.qcc.com/web/search)
- [Tianyancha search](https://www.tianyancha.com/search)
- [AiQicha search](https://www.aiqicha.com/search)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text with sectioned company information and source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Networked lookup results depend on Tavily search responses and public data availability.]

## Skill Version(s):

1.2.1 (source: server release evidence; artifact package metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
