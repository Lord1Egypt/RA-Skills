## Description:

Access lottery data and services through x402.lotto, including listing lotteries, fetching jackpots, purchasing tickets, checking ticket status, and reading draw results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanemort1982](https://clawhub.ai/user/shanemort1982)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover lotteries, retrieve jackpot and result data, and interact with ticket endpoints for x402.lotto. The workflow may involve x402 payment requests using USDC on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable USDC payments without clearly requiring user confirmation or spend limits.

Mitigation: Use a limited wallet or test funds, confirm which x402.lotto endpoints charge USDC before calling them, and avoid granting access to wallet keys that can spend more than intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shanemort1982/skills/x402-lotto)
- [x402 Lotto API example](https://x402.lotto/api/jackpot/eurojackpot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe x402 payment calls that require wallet credentials and USDC spending controls.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
