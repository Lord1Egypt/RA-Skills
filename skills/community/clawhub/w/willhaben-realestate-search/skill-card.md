## Description:

Search willhaben.at real estate listings (apartments, houses) via their public webapi. No browser needed. Search any Austrian state and district with price/room filters. Get full listing details including heating type, building condition, energy class (HWB/fGEE), parking, and floor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mihaimacarie98](https://clawhub.ai/user/mihaimacarie98)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Austrian willhaben.at real estate listings for apartments or houses and retrieve listing details such as price, rooms, area, heating, energy class, parking, condition, and floor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, location filters, and listing identifiers are sent to willhaben.at during use.

Mitigation: Confirm that the agent should use willhaben.at before sending Austrian property query details externally.

Risk: The skill depends on local Python execution and outbound requests to willhaben.at.

Mitigation: Install only in environments where local Python execution and willhaben.at network access are expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mihaimacarie98/skills/willhaben-realestate-search)
- [Publisher profile](https://clawhub.ai/user/mihaimacarie98)
- [willhaben.at search webapi endpoint](https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/{type}/{state}/{district})
- [willhaben.at detail webapi endpoint](https://www.willhaben.at/webapi/iad/atverz/{ad_id})

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Text or JSON results, with Markdown usage examples and shell commands in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs listing summaries and optional detail fields fetched from willhaben.at.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
