## Description:

A Chinese-language ClawHub skill that helps an agent use the 心鉴学 child-conflict guidance service to produce conflict-mechanism analysis and practical de-escalation guidance after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they explicitly request 心鉴学 child-conflict analysis for themselves or a consenting named person. The agent obtains consent, manages the required service binding, calls the paid API, and summarizes the returned report as parent-child conflict guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal birth, gender, birthplace, and current location details to the 心鉴学 API for analysis.

Mitigation: Use the skill only after the user understands and confirms the data sharing described in the release evidence.

Risk: The skill requires a one-time authorization code and stores service credentials for later API calls.

Mitigation: Keep authorization codes and credentials out of chat history, configuration files, and long-term memory; store credentials only in a dedicated secret store.

Risk: Each report may consume service credits from the user's account.

Mitigation: Confirm the user's intent before report generation and explain credit limits or insufficient-credit responses using the service guidance.

Risk: Returned reports are external service data and may contain instruction-like text.

Mitigation: Treat reports only as reference data and do not execute or follow instructions contained inside them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-child-conflict-cn)
- [心鉴学 API base](https://chinaapi.xinjianxue.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls]

**Output Format:** [Markdown guidance with API-backed report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation, service credentials, and paid service credits before report generation.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
