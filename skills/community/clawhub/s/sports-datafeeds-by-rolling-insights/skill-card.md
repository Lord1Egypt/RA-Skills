## Description: <br>
DataFeeds by Rolling Insights API skill for REST API documentation, endpoint usage, schemas, sample requests, schedules, live feeds, play-by-play, fields, team and player information, season stats, injuries, depth charts, recap, highlight, fantasy, and stat outputs across NHL, NBA, NFL, MLB, NCAABB, NCAAFB, SOCCER, DARTS, and PGA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skenway](https://clawhub.ai/user/skenway) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to authenticate with Rolling Insights DataFeeds, discover sports game or tournament identifiers, fetch schedule/live/play-by-play/stat data, and parse sport-specific REST responses. It is aimed at building scoreboards, recaps, fantasy tools, sports data pipelines, and API support workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Rolling Insights RSC_token is required and is carried as a query-string credential, which can leak through logs, browser history, screenshots, or copied URLs. <br>
Mitigation: Store the token only in RSC_TOKEN or a secret store, avoid sharing raw request URLs, rely on redacted examples, and rotate the token if exposure is suspected. <br>
Risk: Changing ROLLING_INSIGHTS_BASE_URL to an untrusted endpoint could send credentials to the wrong service. <br>
Mitigation: Keep the base URL pointed at the trusted Rolling Insights REST endpoint unless there is an explicit, reviewed reason to override it. <br>
Risk: Sports coverage and payload shapes vary by sport and endpoint, so a generic parser can produce incomplete or misleading results. <br>
Mitigation: Check the per-sport endpoint matrix and response shape references before using player, team, injury, depth chart, play-by-play, or season-stat data. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/skenway/sports-datafeeds-by-rolling-insights) <br>
- [Product and endpoint overview](references/overview.md) <br>
- [Authentication guidance](references/auth.md) <br>
- [REST API reference](references/rest-api-reference.md) <br>
- [Per-sport endpoint matrix](references/sport-endpoints.md) <br>
- [Sport-specific response shapes](references/sport-shapes.md) <br>
- [Common workflows](references/workflows.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [End-to-end examples](references/examples.md) <br>
- [Rolling Insights API Locker registration](https://accounts.rolling-insights.com/register) <br>
- [Rolling Insights REST API base](https://rest.datafeeds.rolling-insights.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose REST endpoint patterns, redacted request examples, sport-specific parsing notes, and credential handling guidance.] <br>

## Skill Version(s): <br>
0.2.0 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
