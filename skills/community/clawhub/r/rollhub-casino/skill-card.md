## Description:

Agent Casino helps agents interact with a provably fair gambling API for dice, coinflip, roulette, deposits, withdrawals, balance checks, and bet verification using real cryptocurrency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rollhub-dev](https://clawhub.ai/user/rollhub-dev)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to register agents, manage balances, place and verify casino bets, and withdraw funds through the Agent Casino API. Because the workflow involves real cryptocurrency gambling, users should confirm legal eligibility and approve each money-moving action before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is for real cryptocurrency gambling and includes high-impact money-moving registration, deposit, bet, and withdrawal commands.

Mitigation: Use it only where gambling is legally allowed, require explicit confirmation for every registration, deposit, bet, and withdrawal, and set strict spending and loss limits before use.

Risk: Commands handle API keys, wallet information, currency, chain, amount, and withdrawal address values.

Mitigation: Keep API keys out of prompts, logs, and source files, and verify currency, chain, amount, and withdrawal address before submitting any transfer.

Risk: The security evidence notes a hard-coded referral code that may financially benefit someone else.

Mitigation: Remove or replace the referral code unless the user intentionally approves it.

## Reference(s):

- [Agent Casino](https://agent.rollhub.com)
- [Agent Casino API Base](https://agent.rollhub.com/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/rollhub-dev/skills/rollhub-casino)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash code blocks and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes real-money gambling API requests and requires an API key, wallet details, and explicit confirmation for registration, deposit, bet, and withdrawal actions.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
