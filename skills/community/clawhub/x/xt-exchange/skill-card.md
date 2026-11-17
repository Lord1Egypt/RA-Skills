## Description:

XT.COM exchange CLI for spot and futures trading through progressive conversation, supporting market data, balances, orders, transfers, and withdrawals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realm520](https://clawhub.ai/user/realm520)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide an agent through XT.COM spot and futures market lookup and authenticated account actions, including balances, order placement and cancellation, transfers, and withdrawal requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or cancel orders, transfer funds between account types, and submit withdrawal requests against a live XT.COM account.

Mitigation: Require explicit user confirmation with complete parameters before authenticated financial actions, and use API keys with only the minimum permissions needed.

Risk: The skill uses XT_ACCESS_KEY and XT_SECRET_KEY and can also read credentials from a local plaintext credentials file.

Mitigation: Prefer environment or platform-managed secrets, avoid printing credential values, and disable withdrawal permission unless it is required.

Risk: Authenticated requests can be redirected by XT_HOST or XT_FUTURES_HOST environment overrides.

Mitigation: Use the default XT.COM hosts for authenticated commands unless the override destination is fully trusted.

## Reference(s):

- [XT Exchange ClawHub Skill](https://clawhub.ai/realm520/skills/xt-exchange)
- [XT spot API base URL](https://sapi.xt.com)
- [XT futures API base URL](https://fapi.xt.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and tabular CLI summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated actions require XT_ACCESS_KEY and XT_SECRET_KEY; some commands can make live financial API calls after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
