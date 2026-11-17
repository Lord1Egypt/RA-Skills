## Description:

Access sports data via TheSportsDB (teams, events, scores).

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to configure TheSportsDB access and generate curl requests for team search, recent scores, and upcoming fixtures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a TheSportsDB API key stored in a local .env file and sends requests to TheSportsDB.

Mitigation: Use a scoped key where available, avoid committing the .env file, and confirm that sending sports-data queries to TheSportsDB is acceptable for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gumadeiras/skills/the-sports-db)
- [Publisher profile](https://clawhub.ai/user/gumadeiras)
- [TheSportsDB team search endpoint example](https://www.thesportsdb.com/api/v1/json/$THE_SPORTS_DB_KEY/searchteams.php?t=Palmeiras)
- [TheSportsDB last events endpoint example](https://www.thesportsdb.com/api/v1/json/$THE_SPORTS_DB_KEY/eventslast.php?id=134465)
- [TheSportsDB next events endpoint example](https://www.thesportsdb.com/api/v1/json/$THE_SPORTS_DB_KEY/eventsnext.php?id=134465)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires THE_SPORTS_DB_KEY and notes a 30 requests/minute rate limit.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
