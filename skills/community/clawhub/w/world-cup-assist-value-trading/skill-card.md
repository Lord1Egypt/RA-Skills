## Description: <br>
Scans World Cup Most Assists markets on Simmer, compares market price to FBref-based form value, and prints buy signals for 8%+ discounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxhejohansen-boop](https://clawhub.ai/user/maxhejohansen-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-signal builders use this skill to scan Simmer World Cup Most Assists markets, compare prices against form-based assist estimates, and produce ranked dry-run buy signals for review before any live use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real, potentially irreversible trades when dry-run is disabled. <br>
Mitigation: Keep the skill in dry-run or paper mode unless restricted credentials, position limits, and explicit human review are in place. <br>
Risk: The default fair-value formula is unbacktested and can depend on incomplete web-extracted sports data. <br>
Mitigation: Validate data sources, refresh baselines, backtest the scoring formula, and review every signal before live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maxhejohansen-boop/world-cup-assist-value-trading) <br>
- [Player Baseline Stats](references/player_baselines.md) <br>
- [2024/25 Baseline Refresh Notes](references/2024_25_baseline_refresh.md) <br>
- [2025/26 Baseline Refresh Notes](references/2025_26_baseline_refresh.md) <br>
- [Research Notes and Methodology](references/research_notes.md) <br>
- [FIFA World Cup 2026 Fixtures](references/world_cup_2026_fixtures.md) <br>
- [The Guardian World Cup 2026 fixtures](https://www.theguardian.com/football/world-cup-2026/fixtures) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with terminal text output from a Python signal script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and TAVILY_API_KEY; defaults to dry-run signal printing with capped trade settings.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
