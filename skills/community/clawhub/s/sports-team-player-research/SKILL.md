---
name: sports-team-player-research
description: Build a sourced Flashscore player or team dossier from profiles, squads, career and match records, fixtures, transfers, injury history, and public news. Use for sports roster and career research; source records do not establish fitness, availability, or scouting suitability.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Sports team and player research

Create a source-attributed dossier from Flashscore's public team and player
pages. Start with the sport and entity the user named; keep team and player
identity, season, competition, and observation window explicit. The output is a
description of source records, not a fitness clearance or talent recommendation.

## Resolve the Flashscore identity

1. Use `/flashscore/search` to find a candidate, then verify the result's entity
   type, sport, country, competition, and canonical link. Names can collide
   across youth, reserve, women's, senior, or similarly named teams.
2. Reuse the returned Flashscore ID only with Flashscore routes. Do not pass a
   LiveScore, FotMob, or other provider's ID to these endpoints. Preserve the
   provider ID, URL, retrieval time, and source-reported name.
3. Choose entity routes deliberately: `/flashscore/player` for profile/career,
   `/flashscore/team` and `/flashscore/team-squad` for team context, and
   `/flashscore/entity-news` for Flashscore's own entity-news layout. Team/player
   news routes are third-party headlines and do not include article text.

## Build the requested profile or history

- For team-sport players, use `/flashscore/player-match-log` for recent match
  samples and `/flashscore/player-injuries` or `/flashscore/player-transfers`
  only when requested. Match-log page 1 contains the ten newest rows; later
  pages contain up to 25 older rows. The source has different stat fields by
  sport, and rows without stats may mean unavailable stats, bench, absence, or
  suspension; retain the source label instead of converting every row to zero.
- For individual-sport players, use `/flashscore/player-results` and
  `/flashscore/player-fixtures`; team-sport players do not have those feeds.
  Page until the returned event count is zero. Do not infer inactivity from an
  empty or unsupported endpoint.
- Use `/flashscore/team-fixtures` and `/flashscore/team-results` for bounded
  team form or schedule context. Preserve event date, competition, stage,
  score, and status. Form samples are descriptive, not forecasts.
- `/flashscore/team-squad` returns position-grouped roster entries, season
  statistics, and sometimes absence notes. Its response lists valid per-
  competition scopes; use one of those values. The default is all competitions.
  A source absence note is not a medical report or confirmation that a player
  will miss an upcoming event.
- Team transfers return up to 30 rows per page; paginate until the source has
  no more records. Preserve transfer type and fee text as supplied. Fees may be
  undisclosed, approximate, or in source-specific wording; do not convert them
  into a precise paid amount.
- Injury history and contract/market-value fields are source-reported snapshots.
  Missing records do not prove a player is healthy, available, under contract, or
  worth a particular fee. Use current official club/league evidence for an
  availability claim when the user needs one.
- Entity news, player news, and team news are discovery leads. Preserve
  publisher, date, and link; do not treat a headline as independently verified
  transfer or injury evidence.

```sh
scripts/crawlora.sh /flashscore/search q="Arsenal"
# Use an exact ID from the matching player or team result.
scripts/crawlora.sh /flashscore/team-squad id=example-team-id
scripts/crawlora.sh /flashscore/team-transfers id=example-team-id page=1
scripts/crawlora.sh /flashscore/player id=example-player-id
scripts/crawlora.sh /flashscore/player-match-log id=example-player-id page=1
scripts/crawlora.sh /flashscore/player-results id=example-player-id page=1
```

Return the matched entity and source link, requested season/window, roster or
career evidence, dated records, sample and pagination coverage, and unknowns.
Keep cross-sport stats in their own units and contexts; do not rank players
without the user's criteria and comparable evidence. Do not infer medical
status, employment suitability, or betting outcomes.
