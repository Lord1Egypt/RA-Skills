## Description:

Searches Westin hotels under Marriott and returns live prices, booking links, hotel details, and package offers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-booking assistants use this skill to search Westin hotels by destination, compare current prices, retrieve property details, and surface booking or package links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel search terms, travel dates, destinations, and any configured PROXY_TOKEN may be sent to a hardcoded external proxy.

Mitigation: Install and use this skill only when the operator accepts that disclosure path, and configure PROXY_TOKEN only in environments approved for Westin hotel search.

Risk: Broad trigger wording may invoke the skill for general Westin mentions when the user did not intend a booking search.

Mitigation: Confirm the user wants Westin hotel search, pricing, details, or package links before running network-backed queries.

Risk: Generated answers could misstate live hotel data if they supplement or alter script results.

Mitigation: Present only values returned by the script and avoid adding unsourced prices, ratings, amenities, or booking options.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/westin-hotel-booking)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls]

**Output Format:** [Markdown-formatted hotel search, detail, or package results with booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should preserve script-returned hotel data without adding unsupported prices, ratings, facilities, or properties.]

## Skill Version(s):

1.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
