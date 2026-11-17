## Description:

Query a Yahoo Fantasy Baseball league for rosters, standings, matchups, free agents, draft results, transactions, injuries, and read-only daily roster optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khaney64](https://clawhub.ai/user/khaney64)

### License/Terms of Use:

MIT-0

## Use Case:

Fantasy baseball managers and agents use this skill to inspect Yahoo league data, monitor daily roster availability, and generate lineup, pitcher rotation, and injured-list suggestions without applying roster changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses Yahoo Fantasy Baseball data and stores Yahoo OAuth tokens locally.

Mitigation: Install and authenticate intentionally, use the documented credential path, and protect ~/.openclaw/credentials/yahoo-fantasy/.

Risk: Lineup optimizer output could be mistaken for an applied roster change or definitive instruction.

Mitigation: Treat optimization output as advisory; review suggestions in Yahoo before making any roster move.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/khaney64/skills/yahoo-fantasy-baseball)
- [Yahoo Developer Apps](https://developer.yahoo.com/apps/)
- [yahoo-fantasy-api library](https://github.com/spilchen/yahoo_fantasy_api)
- [MLB Stats API](https://statsapi.mlb.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text, Discord-style Markdown code blocks, and structured JSON depending on the selected command format.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only recommendations; optimization suggestions are advisory and do not apply roster changes.]

## Skill Version(s):

0.1.30 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
