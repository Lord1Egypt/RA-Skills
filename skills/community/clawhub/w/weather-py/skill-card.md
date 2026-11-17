## Description:

Trade Polymarket weather markets using NOAA forecasts via Simmer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnjerry8749](https://clawhub.ai/user/johnjerry8749)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to evaluate, configure, and optionally automate temperature-market trades on Polymarket using Simmer and NOAA weather data. It can also report account balance, open positions, configuration, and dry-run trade opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live Polymarket trades with a Simmer API key.

Mitigation: Use dry-run first, keep max-position and max-trades limits small, and avoid --live until the strategy and account impact are understood.

Risk: The security summary says credential handling is not tightly guarded.

Mitigation: Prefer a narrowly scoped or separate Simmer API key when available, and avoid exposing SIMMER_API_KEY in logs, shared shells, or unattended environments.

Risk: Disabling safeguards or running quiet unattended cron jobs can increase financial risk.

Mitigation: Keep safeguards enabled, avoid --no-safeguards, and review live behavior before using quiet or scheduled runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnjerry8749/skills/weather-py)
- [Publisher profile](https://clawhub.ai/user/johnjerry8749)
- [Simmer API](https://api.simmer.markets)
- [Simmer dashboard](https://simmer.markets/dashboard)
- [NOAA Weather API](https://api.weather.gov)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus plain text console output from the included Python scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; dry-run is the default, while --live can place real trades.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and release changelog mention 1.7.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
