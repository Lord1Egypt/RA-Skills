## Description: <br>
天天条件选基 Skill。使用 FUND_CONDITION_SELECT 能力按基金分类、风险等级、费率、收益和回撤等条件进行筛选，返回候选基金与关键分析字段。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yemeng831-cloud](https://clawhub.ai/user/yemeng831-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query Tiantian Funds condition-based fund screening by category, risk level, fee, return, drawdown, and related filters. The skill helps summarize candidate funds and key returned fields while noting that results are not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security verdict is suspicious and the authoritative guidance warns about broad local access in related ClawHub maintenance behavior. <br>
Mitigation: Use only in a trusted ClawHub maintenance context, review the exact action before execution, and avoid broad access modes unless intentionally required. <br>
Risk: The skill requires an API key for Tiantian Funds and calls an external API endpoint. <br>
Mitigation: Require `TTFUND_APIKEY` before any request, place it only in the `X-API-Key` header, and stop rather than calling the service when the key is missing. <br>
Risk: Fund screening output could be mistaken for investment advice. <br>
Mitigation: Present results as data returned for the current query, avoid fabricating missing values, and state that the output does not constitute investment advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yemeng831-cloud/ttfund-condition-select) <br>
- [Tiantian Funds Skill Invoke API](https://skills.tiantianfunds.com/ai-smart-skill-service/openapi/skill/invoke) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON request bodies, curl commands, and summarized API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the TTFUND_APIKEY environment variable and returns selected fund fields from an external API when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
