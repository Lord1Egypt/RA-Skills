## Description:

Searches Tongcheng travel inventory across hotels, flights, trains, buses, attraction tickets, transport options, and vacation packages, returning prices, details, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search Tongcheng travel products and compare prices, schedules, ratings, availability, and booking links. It supports lookup and comparison only; booking and payment are completed on Tongcheng pages reached from returned links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel search details, including cities, dates, and free-form preferences, are sent to a cloud proxy before reaching Tongcheng APIs.

Mitigation: Do not enter sensitive personal details in free-form fields, and review returned booking links before leaving the agent.

Risk: Prices and availability can change before checkout.

Mitigation: Confirm final prices, availability, and terms on the official Tongcheng booking page before booking or payment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/tongcheng-travel-assistant)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown text with travel result lists, prices, ratings, schedules, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited by category, commonly returning the top 8 to 15 items.]

## Skill Version(s):

1.2.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
