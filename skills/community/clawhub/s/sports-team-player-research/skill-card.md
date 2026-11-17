## Description:

Builds a sourced Flashscore team or player dossier from profiles, rosters, career and match records, fixtures, transfers, injury history, and public news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Sports researchers, journalists, and fans use this skill to assemble source-attributed team and player histories, rosters, and recent results without treating source records as verified fitness or scouting assessments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and the API key are sent to Crawlora, a third-party service.

Mitigation: Use a dedicated Crawlora API key and do not include sensitive personal notes in query values.

Risk: Source injury and roster records may be mistaken for confirmed medical status or future availability.

Mitigation: Describe records as source-reported snapshots and consult current official club or league information for availability claims.

Risk: News headlines and limited match samples may be mistaken for verified reporting, forecasts, or scouting conclusions.

Mitigation: Link and date source records, state sample limits, and avoid unsupported scouting or betting advice.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/sports-team-player-research)
- [Flashscore endpoint reference](artifact/reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Source-attributed Markdown dossier]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes matched entity and source link, season or observation window, dated records, sample coverage, and unknowns.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
