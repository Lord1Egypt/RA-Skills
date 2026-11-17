## Description:

天天Skills lets an agent use FUND_CONDITION_SELECT to screen funds by category, risk level, fees, returns, and drawdown, then summarize candidate funds and key analysis fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yemeng831-cloud](https://clawhub.ai/user/yemeng831-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query the 天天基金 fund-screening service with selected criteria and summarize returned fund candidates. Results are informational and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screening query parameters and the TTFUND_APIKEY are sent to the external 天天基金 service.

Mitigation: Install only when that external service is intended, keep the API key in the TTFUND_APIKEY environment variable, and avoid sharing sensitive criteria unnecessarily.

Risk: Fund-screening output could be mistaken for investment advice.

Mitigation: Present results as informational analysis and remind users that the output does not constitute investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yemeng831-cloud/skills/ttfund-condition-select)
- [天天基金 skill invocation API](https://skills.tiantianfunds.com/ai-smart-skill-service/openapi/skill/invoke)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and summarized API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TTFUND_APIKEY and sends screening parameters to the external 天天基金 service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
