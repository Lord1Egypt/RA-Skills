## Description:

Searches W Hotels in the Fliggy Marriott catalog and returns current prices, hotel details, package offers, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel agents use this skill to search W Hotels by destination, inspect hotel details, and compare package offers with booking links from the Fliggy Marriott catalog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a local PROXY_TOKEN to a hardcoded external Tencent SCF proxy.

Mitigation: Review the proxy behavior before installation, scope or omit PROXY_TOKEN in the agent environment, and avoid using credentials that are not intended for this service.

Risk: Hotel search parameters and booking queries are sent to an external proxy service.

Mitigation: Use the skill only when that network disclosure is acceptable, and document the proxy dependency for users and operators.

Risk: Hotel prices, ratings, amenities, and booking links could be misrepresented if the agent embellishes script output.

Mitigation: Preserve the script output as the source of truth and do not add unsupported hotels, prices, ratings, amenities, or booking links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/whotels-booking)
- [Publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with hotel listings, booking links, details, package offers, and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should preserve script output without adding unsupported prices, ratings, amenities, or hotels.]

## Skill Version(s):

1.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
