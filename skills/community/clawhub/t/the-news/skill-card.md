## Description:

Gives agents real-time and archival access to front-page headlines across 20 countries for breaking news, current events, and comparative media analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfkislev](https://clawhub.ai/user/sfkislev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current or historical multi-source front-page headline snapshots by country. It supports breaking-news orientation, comparative media analysis, and micro-historical review of headline coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Returned headlines and AI-generated overviews can be incomplete, biased, or misleading if treated as verified facts.

Mitigation: Use raw headlines and original article links as primary evidence, label uncertainty, and verify important claims with original sources.

Risk: Current-events data changes over time and live API responses may differ between calls.

Mitigation: Record the country, mode, query parameters, and timestamps when relying on a specific snapshot or archive result.

## Reference(s):

- [The News on ClawHub](https://clawhub.ai/sfkislev/skills/the-news)
- [The Hear API example](https://www.thehear.org/api/country-view/germany)
- [The Hear web interface example](https://www.thehear.org/en/germany)

## Skill Output:

**Output Type(s):** [guidance, API calls, text, JSON]

**Output Format:** [Markdown guidance with HTTPS API examples and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include third-party headlines, source links, timestamps, subtitles, and AI-generated overviews from a public read-only API.]

## Skill Version(s):

1.0.17 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
