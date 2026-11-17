## Description:

Football Data helps agents answer football/soccer questions using standings, schedules, match stats, xG, transfers, player profiles, lineups, injury news, league tables, and daily fixtures across 13 competitions without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonelli182](https://clawhub.ai/user/antonelli182)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to look up football/soccer standings, fixtures, match summaries, player and team profiles, xG, injury status, and transfer information while staying within documented league and endpoint coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can install unpinned remote Python code if the package install fails.

Mitigation: Use a restricted virtual environment or container, prefer a pinned reviewed sports-skills release or commit, and require explicit approval before using the GitHub fallback.

Risk: The skill may produce incomplete or incorrect results when commands are used outside documented coverage, such as xG outside top-five leagues or Premier League-only endpoints for other leagues.

Mitigation: Check the data coverage reference before endpoint selection and fall back to broadly supported schedule, standings, summary, timeline, or team-search commands when narrow endpoints are unavailable.

Risk: The documentation marks get_head_to_head as listed but unavailable, which can cause command selection confusion.

Mitigation: Do not call get_head_to_head; compare overlapping team schedules manually instead.

Risk: Very recent match xG data may lag 24 to 48 hours after a match.

Mitigation: Report the lag clearly and retry later or provide non-xG match statistics when xG data is not indexed yet.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antonelli182/skills/sports-skills-football-data)
- [Football Data API Reference](artifact/references/api-reference.md)
- [Football Data Valid Commands & Common Mistakes](artifact/references/commands.md)
- [Football Data Data Coverage by League](artifact/references/data-coverage.md)
- [Football Data JSON Schemas](artifact/references/schemas.md)
- [Machina Sports](https://machina.gg)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration instructions]

**Output Format:** [Markdown with inline shell commands, Python examples, and structured data guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should respect documented command availability, league coverage, season ID rules, and post-match data limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
