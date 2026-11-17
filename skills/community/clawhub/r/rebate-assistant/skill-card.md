## Description:

Rebate Assistant routes Chinese shopping and account requests through authorization/tutorial, product-link rebate, and product-search rebate flows for Taobao, JD, and Pinduoduo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyfile](https://clawhub.ai/user/skyfile)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to authorize a WeChat-linked rebate account, search for rebate-eligible products, convert Taobao, JD, and Pinduoduo links into rebate links, check balances, and submit withdrawal requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store OpenID, shopping requests, balances, and pending withdrawal data locally.

Mitigation: Use it only in a trusted workspace, avoid shared machines, and clear local skill data when account state should no longer persist.

Risk: The skill relies on a rebate backend and hardcoded WeChat/public-account URLs for account and rebate flows.

Mitigation: Install only if those services are trusted, and verify generated rebate, authorization, and account-detail links before relying on them.

Risk: The skill can submit a withdrawal after a prepared amount and a confirmation phrase.

Mitigation: Require explicit user confirmation, review the withdrawal amount before confirmation, and rely on backend account controls for final authorization.

Risk: The skill can use the configured model API key for product-search intent parsing.

Mitigation: Use a scoped model provider configuration, monitor API usage, and avoid sending shopping queries that should remain private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skyfile/skills/rebate-assistant)
- [Publisher profile](https://clawhub.ai/user/skyfile)
- [Rebate backend service](https://rebate-skill.io.mlj130.com)
- [WeChat authorization page](https://xiaomaxiangshenghuo.io.mlj130.com/authlogin.html)
- [Public account follow page](https://xiaomaxiangshenghuo.io.mlj130.com/follow.html)
- [Rebate details page](https://xiaomaxiangshenghuo.io.mlj130.com/rebate-details.html)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, guidance]

**Output Format:** [Markdown user-facing responses, with JSON available from CLI and debugging flows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes one user message at a time across authorization/tutorial, product search, product-link rebate, balance, and withdrawal flows.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
