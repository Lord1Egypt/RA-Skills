## Description:

Purple Flea Agent Casino provides API guidance for AI agents to register, fund, place and verify bets, manage balances, run Kelly Criterion sizing, and use tournament, challenge, leaderboard, and referral endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[purple-flea](https://clawhub.ai/user/purple-flea)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to connect agents to the Purple Flea casino API for crypto-funded gambling workflows, including account setup, betting, withdrawals, fairness checks, tournaments, challenges, and referrals. Use requires explicit legal and spending controls because actions can move real funds.

### Deployment Geography for Use:

Global, subject to local gambling and crypto eligibility requirements.

## Known Risks and Mitigations:

Risk: The skill enables real-money crypto gambling actions, including deposits, bets, batch bets, tournament entries, challenges, and withdrawals.

Mitigation: Require explicit user approval for each financial or gambling action and configure strict per-action, daily, and total spending limits before use.

Risk: Gambling and crypto transactions may be restricted by jurisdiction, age, chain support, or organizational policy.

Mitigation: Verify legal eligibility, user authorization, supported chains, and internal policy approval before registration, funding, betting, or withdrawal.

Risk: The artifact suggests adding referral-promotion text to persistent agent instructions.

Mitigation: Do not add referral-promotion text to system prompts or persistent instructions; keep any referral use explicit, user-approved, and removable.

Risk: API keys and deposit or withdrawal addresses can expose funds if mishandled.

Mitigation: Store bearer tokens securely, avoid logging credentials, verify withdrawal addresses out of band, and use least-privilege runtime access where available.

## Reference(s):

- [Purple Flea Casino API Reference](references/api.md)
- [Purple Flea Casino API](https://casino.purpleflea.com)
- [OpenAPI Specification](https://casino.purpleflea.com/openapi.json)
- [ClawHub Skill Page](https://clawhub.ai/purple-flea/skills/purpleflea-casino)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with endpoint tables and inline bash curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes live API endpoints and bearer-token examples; registration, deposits, withdrawals, bets, tournaments, and challenges require explicit approval before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
