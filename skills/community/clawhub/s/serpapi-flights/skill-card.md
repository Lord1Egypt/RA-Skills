## Description:

Query Google Flights via SerpApi for flight schedules, prices, and cabin class info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kirorab](https://clawhub.ai/user/kirorab)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to look up Google Flights results through SerpApi for route schedules, cabin-class comparisons, prices, aircraft, and delay indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a SerpApi key for flight searches.

Mitigation: Provide the key through the documented environment variable and avoid exposing it in prompts, logs, or shared outputs.

Risk: Flight searches can consume SerpApi quota.

Mitigation: Check route, date, and cabin options before running queries, especially when using all-class searches.

Risk: Google Flights prices and availability can differ from airline-direct purchase flows.

Mitigation: Treat returned prices as search guidance and verify fare details with the booking provider before purchase.

Risk: Default output is Chinese-oriented unless language and currency options are changed.

Mitigation: Set language and currency options explicitly when the user needs localized output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kirorab/skills/serpapi-flights)
- [SerpApi search endpoint](https://serpapi.com/search.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown table by default, or raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are route, date, passenger, cabin class, currency, language, and stop-filter dependent.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
