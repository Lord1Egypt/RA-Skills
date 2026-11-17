## Description:

Track accumulator (acca) betting slips across football, basketball, and tennis by parsing slip photo or text, checking live scores every 15 minutes, and reporting bet status with overall acca health and cash-out context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[svenmedina07-ship-it](https://clawhub.ai/user/svenmedina07-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to monitor accumulator or parlay betting slips across football, basketball, and tennis, with parsed leg summaries, live score checks, bet status, and rough cash-out context. It is for score monitoring and status reporting, not betting or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring tracking jobs may continue checking scores and generating reports after setup.

Mitigation: Confirm the parsed slip before starting, use bounded schedules and repeat counts, and stop tracking when no longer needed.

Risk: Betting-slip reports may be written to local cron output and could include wagering details or stake amounts.

Mitigation: Use the skill only where local report storage is acceptable and avoid sharing sensitive betting information unnecessarily.

Risk: Cash-out values and score status can be rough or unavailable when live-score data is delayed, missing, or bookmaker rules differ.

Mitigation: Treat outputs as score-monitoring guidance, never financial advice; verify slip parsing, live scores, and bookmaker rules before acting.

## Reference(s):

- [Bet Type Reference](references/bet-types.md)
- [Data Source Strategy](references/data-sources.md)
- [ClawHub Skill Page](https://clawhub.ai/svenmedina07-ship-it/skills/sports-acca-tracker)
- [TheSportsDB eventsday API](https://www.thesportsdb.com/api/v1/json/3/eventsday.php)
- [ESPN Basketball Scoreboard API](https://site.api.espn.com/apis/site/v2/sports/basketball/${path}/scoreboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with tables and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create bounded recurring score-check jobs and local betting-slip report files; no API keys are required by the bundled score helper.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
