## Description:

Search realestate.com.au property listings by constructing search and listing URLs. Use when searching for Australian properties to buy, rent, or sold via realestate.com.au. Supports building filtered search URLs (suburb, price, bedrooms, property type, multiple suburbs) and individual listing URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakelin](https://clawhub.ai/user/jakelin)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to construct realestate.com.au URLs for Australian property searches, sold-property searches, individual listings, suburb profiles, and pagination. It is useful when direct page fetching is unavailable or rate limited and a browser-ready search URL is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DuckDuckGo site-search fallback sends property search terms to DuckDuckGo.

Mitigation: Avoid the fallback for sensitive searches, or review search terms before sending them to a third-party search service.

Risk: DuckDuckGo fallback results may be incomplete and direct realestate.com.au fetching is commonly rate limited or blocked.

Mitigation: Use generated realestate.com.au URLs in a browser for complete search review, and treat fallback listing snippets as partial discovery results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jakelin/skills/rea-search)
- [realestate.com.au buy search URL pattern](https://www.realestate.com.au/buy/property-{types}-{filters}-in-{location}/list-{page})
- [realestate.com.au sold search URL example](https://www.realestate.com.au/sold/property-house-in-malvern,+vic+3144/list-1)
- [realestate.com.au suburb profile URL example](https://www.realestate.com.au/neighbourhoods/malvern-3144-vic)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with URL patterns and inline examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser-ready realestate.com.au URLs and optional DuckDuckGo site-search guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
