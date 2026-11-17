## Description:

Provides real-time football match data and structured betting analysis for European leagues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lysandre2007](https://clawhub.ai/user/lysandre2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve upcoming and live European football data, compare form, head-to-head results, standings, lineups, statistics, and odds, then produce structured betting-pronostic summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a RapidAPI credential and can send it to an environment-configured host.

Mitigation: Run only where RAPIDAPI_HOST is controlled or allowlisted, and provide credentials only in trusted environments.

Risk: Football-related prompts and requests may be sent to a RapidAPI football data service.

Mitigation: Avoid sending confidential user context with sports queries and disclose external data-service use where required.

Risk: Sports betting recommendations can be affected by stale, incomplete, or changing match, odds, and lineup data.

Mitigation: Treat outputs as decision support and verify current data, odds, and applicable betting requirements before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lysandre2007/skills/sports-pronostics)
- [Publisher profile](https://clawhub.ai/user/lysandre2007)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown-formatted football analysis with tables, confidence ratings, risk notes, and betting recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RapidAPI key and a controlled RapidAPI host configuration to retrieve live football data.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact export)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
