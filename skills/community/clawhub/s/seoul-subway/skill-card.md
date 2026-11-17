## Description:

Seoul Subway assistant for real-time arrivals, route planning, and service alerts (Korean/English)

This skill is ready for commercial/non-commercial use.

## Publisher:

[dukbong](https://clawhub.ai/user/dukbong)

### License/Terms of Use:


## Use Case:

External users and transit-focused agents use this skill to answer Seoul Subway questions about arrivals, routes, station details, service alerts, last trains, exits, accessibility, quick exits, and restrooms in Korean or English.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transit queries are sent to the disclosed proxy service.

Mitigation: Allow the proxy for a session, or persistently only if the user trusts the publisher-operated proxy; avoid placing sensitive information in station or route search terms.

Risk: Transit answers depend on remote proxy availability and the freshness of upstream transit data.

Mitigation: Treat urgent travel decisions as advisory and verify critical route, alert, accessibility, or last-train information with an official transit source when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dukbong/skills/seoul-subway)
- [Project homepage](https://github.com/dukbong/seoul-subway)
- [Proxy API base URL](https://vercel-proxy-henna-eight.vercel.app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown responses with bilingual tables and concise transit guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live arrival, route, station, alert, last-train, exit, accessibility, quick-exit, and restroom details.]

## Skill Version(s):

0.1.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
