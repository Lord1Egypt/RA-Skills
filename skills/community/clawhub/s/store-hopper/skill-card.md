## Description:

Store Hopper helps plan efficient one-day city store-hopping routes by combining weather checks, local guide search, page fetching, and route planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziyou979](https://clawhub.ai/user/ziyou979)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan same-day food, cafe, dessert, shopping, or photo-stop itineraries after providing a city or area, preferences, time window, and optional start point.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send city names, addresses, search terms, and fetched URLs to external weather, search, map, and reader services.

Mitigation: Use it only with location and URL data that can be shared with those providers, and avoid private or sensitive trip details.

Risk: The fetch workflow can request arbitrary webpages through anti-bot and proxy services.

Mitigation: Do not provide private, signed, internal, localhost, or token-bearing URLs; run the skill in a restricted environment when reviewing untrusted pages.

Risk: Route quality depends on third-party geocoding and map services, with optional API keys improving accuracy.

Mitigation: Pin dependencies, provide your own map API keys when needed, and review generated routes before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziyou979/skills/store-hopper)
- [City code table](artifact/data/city-codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown itinerary with supporting JSON-producing script calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes weather summary, stop-by-stop route details, schedule, distance, estimated costs, and practical tips.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
