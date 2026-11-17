## Description:

Pulls sports scores, standings, rosters, player/team stats, public sports news, editorial, wiki/video content, and betting odds through the Crawlora API — ESPN, SofaScore, MLB, Strava, DraftKings Sportsbook, Cricinfo, and Sportskeeda. Use for scores/stats or explicitly requested public sports-media research; Strava routes and clubs can reveal location-sensitive patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Sports fans, analysts, and researchers use the skill to look up scores, standings, rosters, statistics, public sports coverage, and sportsbook odds across supported providers. It can also find public Strava routes and clubs when relevant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send the Crawlora API key and query details to Crawlora; the security scan reports partial coverage because one local reference could not be resolved.

Mitigation: Use the key only in a trusted environment, keep it out of shared prompts and files, avoid confidential query targets, and review the unresolved reference before relying on the release.

Risk: Public Strava routes and club information can reveal location-sensitive training patterns.

Mitigation: Use these lookups only for relevant public sports research and do not infer a person's home, routine, or sensitive location history.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [Crawlora documentation](https://crawlora.net/docs?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills)
- [Crawlora playground](https://crawlora.net/playground?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis, Guidance]

**Output Format:** [Normalized JSON data with concise text summaries or research guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coverage and freshness vary by provider and endpoint; live scores reflect each source's update cadence.]

## Skill Version(s):

1.0.25 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
