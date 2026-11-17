## Description:

Trades Polymarket weather markets using NOAA forecasts, dynamic confidence modeling, quality filtering, and configurable safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohamedj2020](https://clawhub.ai/user/mohamedj2020)

### License/Terms of Use:


## Use Case:

External users with a Simmer API key use this skill to inspect positions and manually or on a schedule execute weather-market trades based on NOAA forecasts and configured risk limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place automated real-money trades without per-trade approval after live trading or scheduled execution is enabled.

Mitigation: Keep autostart disabled until reviewed, test with dry-run and status commands first, use a small balance, and keep the configured per-trade and per-run limits conservative.

Risk: A Simmer trading API key is required and the security guidance identifies credential-handling weaknesses.

Mitigation: Use a least-privilege trading-only key with no withdrawal or account-admin rights, store it locally, rotate it after testing, and address the authenticated redirect handling concern before using meaningful funds.

Risk: The optional tradejournal dependency may introduce additional network behavior if installed.

Mitigation: Do not enable the optional dependency unless its source and network behavior have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohamedj2020/skills/weather-trader)
- [Publisher profile](https://clawhub.ai/user/mohamedj2020)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [Simmer dashboard](https://simmer.markets/dashboard)
- [Simmer API endpoint](https://api.simmer.markets)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and console text from Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; live trading is controlled by --live or by manually enabling scheduled execution.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
