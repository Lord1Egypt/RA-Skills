## Description:

Fetches live theme park wait times and park metadata from Queue-Times.com JSON APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adaclaw](https://clawhub.ai/user/adaclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to resolve theme park IDs, fetch public wait-time and status data, and summarize ride waits, closures, and park metadata from Queue-Times.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public wait-time data may be delayed or differ from official park operations.

Mitigation: State the approximate five-minute refresh cadence and verify important park details against official park sources when accuracy matters.

Risk: User-facing output that displays API data may omit the required Queue-Times.com attribution.

Mitigation: Include a prominent Powered by Queue-Times.com link whenever presenting wait-time or park data.

Risk: Broad park-name or region queries may match the wrong park.

Mitigation: Resolve parks through parks.json using park name, country, and operator group clues; clarify ambiguous matches before summarizing live waits.

## Reference(s):

- [Queue Times API documentation](https://queue-times.com/pages/api)
- [Queue-Times.com](https://queue-times.com/)
- [ClawHub skill page](https://clawhub.ai/adaclaw/skills/theme-park-queue-times)
- [Queue Times reference excerpts](artifact/reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text summaries with Queue-Times.com attribution and, when useful, referenced API URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Queue-Times.com API data that refreshes about every five minutes; last_updated values are UTC.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
