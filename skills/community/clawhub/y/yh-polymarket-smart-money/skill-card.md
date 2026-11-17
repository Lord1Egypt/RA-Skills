## Description:

Trade Polymarket markets where PolyClawster whale signals are active by fetching smart money signals and preparing YES/NO trades when configured thresholds are met.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhlorra](https://clawhub.ai/user/yhlorra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan Polymarket markets for PolyClawster smart-money signals, review high-conviction opportunities, and optionally execute trades through Simmer when live mode is enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can submit real-money Polymarket trades using externally supplied signals with limited validation or confirmation.

Mitigation: Start in dry-run mode or TRADING_VENUE=sim, use low and revocable trading limits, and review each signal source before enabling --live.

Risk: The skill requires a Simmer API key and can use an overridden SMART_MONEY_API_URL endpoint.

Mitigation: Use a scoped or revocable API key, avoid untrusted signal endpoints, and pin dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yhlorra/skills/yh-polymarket-smart-money)
- [Publisher Profile](https://clawhub.ai/user/yhlorra)
- [PolyClawster Signals API](https://polyclawster.com/api/signals)
- [Simmer Dashboard](https://simmer.markets/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, environment-variable configuration, and console trading status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; supports dry-run mode, live trading mode, minimum signal score, and position status commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
