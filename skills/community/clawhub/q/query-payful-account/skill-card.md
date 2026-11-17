## Description:

Query Payful account information including balance, transactions, and account details using Payful session credentials supplied through environment variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hugogu](https://clawhub.ai/user/hugogu)

### License/Terms of Use:

MIT-0

## Use Case:

External users or agents use this skill to check Payful account balance and account details after supplying required Payful browser-session credentials in a trusted environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses sensitive Payful browser-session credentials that can grant account access.

Mitigation: Run only in a trusted environment, do not share PAYFUL_TOKEN or PAYFUL_USER_ID, and prefer scoped read-only credentials where available.

Risk: The custom API URL option can send Payful session cookies to an unverified host.

Mitigation: Do not invoke --api-url with unverified hosts; prefer a version that removes custom endpoints or restricts them to an allowlist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hugogu/skills/query-payful-account)
- [Payful account balance endpoint](https://global.payful.com/api/user/account/queryUserAccBalByHomePage)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text balance summary or JSON account data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PAYFUL_TOKEN and PAYFUL_USER_ID credential environment variables.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
