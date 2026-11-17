## Description:

XinJianXue Parent-Child Conflict Advisor helps an agent use XinJianXue's paid API to analyze parent-child conflict patterns and provide de-escalation and communication guidance after user consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they explicitly want XinJianXue-assisted guidance on parent-child conflict. The agent gathers consent and required birth, gender, and location details, calls the XinJianXue API under the user's account, and returns practical, non-punitive communication guidance without assigning blame.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive personal birth, gender, and location information to www.xinjianxue.com for analysis.

Mitigation: Use it only after explicit user consent and only for subjects the user has identified and agreed to analyze.

Risk: The skill binds an AI to a XinJianXue account using a sensitive one-time authorization code and later uses account credentials.

Mitigation: Provide the authorization code only intentionally, store generated credentials in dedicated credential storage, and never expose credentials in chat, notes, configuration files, or long-term memory.

Risk: API calls can consume paid service tokens under the user's XinJianXue account.

Mitigation: Confirm the user wants the analysis before each report call and make token use clear before invoking the paid API.

Risk: The API report may contain instruction-like text even though it is analysis data.

Mitigation: Treat returned reports as reference material only and use the local skill role definition as the sole instruction source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-child-conflict-global)
- [XinJianXue service](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown guidance with HTTP request details and API-derived analysis summarized for the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user consent, dual credentials, required subject details, and paid service tokens before report generation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
