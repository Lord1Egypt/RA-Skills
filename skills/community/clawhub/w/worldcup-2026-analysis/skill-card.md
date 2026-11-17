## Description:

Provides Chinese-language quantitative football and World Cup 2026 analysis using Elo ratings, Dixon-Coles Poisson scoring, Monte Carlo simulation, searchable live calibration, and optional odds APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luciuszhao0101-dot](https://clawhub.ai/user/luciuszhao0101-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate football match forecasts, score-probability summaries, group or knockout advancement estimates, upset analysis, odds-value checks, and calibration notes. It is framed as an analytics aid and not as betting advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional API credentials may be exposed through request URLs or local process/cache handling.

Mitigation: Use scoped, revocable API keys; avoid logging generated URLs; rotate keys if command output or cache data is shared.

Risk: Calibration commands can modify local Elo ratings, team statistics, schedule data, and calibration logs.

Mitigation: Review source data before calibration, keep generated backups, and compare changed files before relying on updated predictions.

Risk: The skill can over-trigger on broad football or odds-analysis prompts and produce probabilistic outputs that may be mistaken for betting advice.

Mitigation: Use it only for football analytics workflows, require source-backed live facts, and preserve the non-betting-advice disclaimer in user-facing outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luciuszhao0101-dot/skills/worldcup-2026-analysis)
- [The Odds API](https://the-odds-api.com)
- [football-data.org](https://www.football-data.org)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown analysis with probability tables, score summaries, cited calibration notes, and optional command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include data cutoff time, source notes for live facts, and a reminder that results are statistical analysis rather than betting advice.]

## Skill Version(s):

2.1.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
