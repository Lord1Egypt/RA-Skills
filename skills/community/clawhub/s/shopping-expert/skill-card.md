## Description:

Find and compare products online through Google Shopping and locally through nearby store search, ranking results by price, ratings, availability, reviews, shipping or distance, and stated preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[udiedrichsen](https://clawhub.ai/user/udiedrichsen)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find product options, compare prices and ratings, generate ranked shopping lists, and locate nearby stores when a location is provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping searches are sent to SerpAPI for online results.

Mitigation: Avoid entering sensitive or private product queries unless sharing them with SerpAPI is acceptable.

Risk: Location text is sent to Google Places when local or hybrid search is used.

Mitigation: Use city-level or approximate locations when precise location sharing is unnecessary.

Risk: Local store results are nearby store suggestions and do not confirm product stock.

Mitigation: Verify inventory and details with the store before relying on a local result.

Risk: Buy and directions links are returned from external shopping and map sources.

Mitigation: Review links before opening them and confirm price, seller, and destination details before purchase or travel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/udiedrichsen/skills/shopping-expert)
- [Publisher profile](https://clawhub.ai/user/udiedrichsen)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown shopping table by default, or structured JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ranked products or stores, prices or distances, ratings, availability, source names, buy or directions links, warnings, and a timestamp.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
