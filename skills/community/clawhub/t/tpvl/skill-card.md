## Description:

TPVL (Taiwan Professional Volleyball League) stats, scores, schedules, and standings for Taiwan's pro volleyball.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ichendong](https://clawhub.ai/user/ichendong)

### License/Terms of Use:

MIT

## Use Case:

Volleyball fans, analysts, and other external users can query Taiwan Professional Volleyball League game results, schedules, standings, and player statistics by season, team, date, or category.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cached scores, schedules, or standings may be up to 30 minutes old.

Mitigation: Check the TPVL official site for the latest information when timing or live status matters.

Risk: The skill installs its requests dependency and fetches public data from tpvl.tw.

Mitigation: Review the dependency installation and allow the outbound request when league data is needed; no API key or account login is required.

## Reference(s):

- [TPVL matches and schedules](https://tpvl.tw/matches)
- [TPVL standings](https://tpvl.tw/standings)
- [TPVL player statistics](https://tpvl.tw/stats/players)
- [API discovery notes](references/api-discovery.md)
- [ClawHub release page](https://clawhub.ai/ichendong/skills/tpvl)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON by default, or readable text when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can be filtered by season, date, team, and statistic category; cached responses may be up to 30 minutes old.]

## Skill Version(s):

1.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
