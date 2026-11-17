## Description:

Covers the DataFeeds by Rolling Insights sports API end-to-end: getting live scores, schedules, stats, play-by-play, and player data across major leagues (NFL, NBA, MLB, NHL, NCAA, Soccer, PGA, Darts).

This skill is ready for commercial/non-commercial use.

## Publisher:

[skenway](https://clawhub.ai/user/skenway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to help agents authenticate to Rolling Insights DataFeeds, discover games and tournaments, call REST endpoints, and turn sport-specific payloads into schedules, live-score summaries, play-by-play recaps, stats lookups, and integration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RSC_token is carried in query strings and can leak through logs, browser history, screenshots, copied URLs, or chat transcripts.

Mitigation: Keep RSC_TOKEN in a local environment variable or secret store, use HTTPS, avoid sharing raw request URLs, preserve token redaction, and rotate the token if exposure is suspected.

Risk: Endpoint availability and payload shape vary by sport, so unsupported endpoint calls or single-schema parsing can produce misleading answers.

Mitigation: Check the endpoint matrix before calling player, team, injury, depth-chart, or play-by-play resources, and parse sport-specific payloads defensively.

Risk: Live sports responses can be stale because of cache behavior.

Mitigation: Use no-cache headers and a timestamp cache buster for live calls, and treat HTTP 304 as a cache problem to retry once rather than as a successful fresh result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skenway/skills/sports-datafeeds-by-rolling-insights)
- [Overview](references/overview.md)
- [Authentication](references/auth.md)
- [REST API Reference](references/rest-api-reference.md)
- [Sports Endpoint Matrix](references/sport-endpoints.md)
- [Sport Shapes](references/sport-shapes.md)
- [Workflows](references/workflows.md)
- [Troubleshooting](references/troubleshooting.md)
- [End-to-End Examples](references/examples.md)
- [Rolling Insights API Locker](https://accounts.rolling-insights.com/register)
- [Breakaway Accelerator](https://rolling-insights.com/breakaway-accelerator/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with endpoint patterns, shell command examples, and JSON-oriented response parsing notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference helper scripts that read RSC_TOKEN, redact the token in logged URLs, and emit raw JSON from Rolling Insights REST endpoints.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
