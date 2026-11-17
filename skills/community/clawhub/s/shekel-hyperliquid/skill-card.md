## Description:

AI-powered perpetual futures trading on Hyperliquid DEX that handles account creation, USDC onboarding, and autonomous trade execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shekel-xyz](https://clawhub.ai/user/shekel-xyz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to configure and operate a Shekel trading agent for Hyperliquid perpetual futures, including onboarding, deposits, strategy updates, runs, schedules, account management, and vault operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trade futures, manage funds, withdraw assets, export wallet key material, and alter account state using a single API key.

Mitigation: Use a dedicated secret manager for the API key, rotate keys exposed in memory or logs, and require fresh user confirmation for withdrawals, wallet export, account deletion, vault operations, schedule changes, and whitelist bypasses.

Risk: Remote instruction updates can change what the agent is told to do after installation.

Mitigation: Review fetched instructions and version changes before use, and require re-review before executing financial actions after material instruction changes.

Risk: Autonomous trading and vault operations can create financial losses or unintended account changes.

Mitigation: Set risk limits, confirm schedules and single-ticker runs, use isolated margin when appropriate, and monitor balances, positions, LLM logs, and performance metrics.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/shekel-xyz/skills/shekel-hyperliquid)
- [Shekel skill endpoint](https://shekel-skill-backend.onrender.com/skill)
- [Shekel dashboard](https://www.shekel.xyz/hl-skill-dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SHEKEL_API_KEY for authenticated operations.]

## Skill Version(s):

1.14.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
