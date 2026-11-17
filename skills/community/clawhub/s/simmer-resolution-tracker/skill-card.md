## Description:

Monitors Simmer positions for resolutions, logs wins and losses to a trade journal, automatically redeems winning Polymarket positions on-chain, and sends Discord webhook alerts every 5 minutes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djdyll](https://clawhub.ai/user/djdyll)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Simmer users use this skill to monitor resolved Polymarket positions, update trade records, receive Discord alerts, and redeem eligible winning positions automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release automates wallet-affecting redemptions and requires both an API key and wallet private key.

Mitigation: Install only in an isolated environment with a dedicated low-balance wallet and narrowly scoped API key.

Risk: Broad credential exposure and weak safety boundaries may increase impact if local environment files or scheduled execution are misconfigured.

Mitigation: Avoid storing unrelated secrets in ~/.env, confirm cron, DATA_DIR, and DISCORD_WEBHOOK settings before live use, and review the environment used by the scheduled process.

Risk: Live mode can perform on-chain redemptions through the simmer-sdk dependency.

Mitigation: Run POLY_MODE=sim first, then pin and review simmer-sdk before enabling live redemptions.

## Reference(s):

- [Simmer Resolution Tracker on ClawHub](https://clawhub.ai/djdyll/skills/simmer-resolution-tracker)
- [Simmer](https://www.simmer.markets/)
- [Simmer API endpoint](https://api.simmer.markets)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown instructions, shell commands, Python execution output, JSONL/JSON state files, and Discord webhook messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and WALLET_PRIVATE_KEY; optional DISCORD_WEBHOOK, POLY_MODE, and DATA_DIR; intended cron cadence is every 5 minutes.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
