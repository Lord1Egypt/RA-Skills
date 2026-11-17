## Description:

Provides a Chinese classmate-relationship Q&A advisor that, after user confirmation and account binding, calls the Xinjianxue API to generate school peer relationship guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they explicitly choose the Xinjianxue classmate-relationship advisor for questions about school peer relationships, exclusion, gossip, or trouble making friends. The agent collects required consent and profile details, calls the paid Xinjianxue API, and returns practical guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive profile details and uses account-bound credentials with the Xinjianxue API.

Mitigation: Obtain explicit user consent before use, treat the authorization code, license, and api_key as secrets, and store credentials only in dedicated secret storage.

Risk: The API response may contain report content that should not become executable instructions.

Mitigation: Use returned reports only as data or reference material and keep the local skill instructions as the sole instruction source.

Risk: The service may consume paid or limited account credits.

Mitigation: Tell users that API calls can consume Xinjianxue credits and surface credit-shortage guidance from the service when applicable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-classmate-qa-cn)
- [Xinjianxue API base](https://chinaapi.xinjianxue.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text guidance derived from Xinjianxue API report data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation, account binding, sensitive profile details, and paid API credits before report generation.]

## Skill Version(s):

2.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
