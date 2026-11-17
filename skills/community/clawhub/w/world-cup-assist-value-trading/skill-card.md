## Description:

Scans World Cup Most Assists markets on Simmer, compares market price to FBref-based form value, and prints buy signals for 8%+ discounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxhejohansen-boop](https://clawhub.ai/user/maxhejohansen-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-tool builders use this skill to have an agent inspect World Cup Most Assists markets, compare market probabilities against form-derived estimates, and print ranked buy signals for review. The artifact presents the strategy as a dry-run-first framework, not as a validated production trading system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money trades using Simmer credentials, and on-chain orders cannot be recalled.

Mitigation: Keep dry-run enabled until the strategy is audited, require explicit live-mode confirmation, and add cumulative spend and position limits before scheduling live runs.

Risk: The signal depends on fragile web-search sports data and an unbacktested fair-value formula.

Mitigation: Validate source data before acting, prefer structured baselines or reliable direct data providers, and backtest the formula before using it for live decisions.

Risk: Trading and search API keys are required for operation.

Mitigation: Use dedicated low-limit Simmer and Tavily keys, run the skill in an isolated environment, and pin dependencies before installation.

## Reference(s):

- [Player Baseline Stats](references/player_baselines.md)
- [2024/25 Baseline Refresh Notes](references/2024_25_baseline_refresh.md)
- [2025/26 Baseline Refresh Notes](references/2025_26_baseline_refresh.md)
- [Research Notes and Methodology](references/research_notes.md)
- [FIFA World Cup 2026 Fixtures](references/world_cup_2026_fixtures.md)
- [ClawHub Skill Page](https://clawhub.ai/maxhejohansen-boop/skills/world-cup-assist-value-trading)
- [Publisher Profile](https://clawhub.ai/user/maxhejohansen-boop)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown guidance with Python code and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; ranked signals are capped at five per run and live trades require explicit code/configuration changes.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
