## Description:

Searches Sheraton hotels in the Marriott portfolio, returning current prices, booking links, hotel details, and package offers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel agents use this skill to look up Sheraton hotel availability, prices, booking links, hotel details, and package offers from the configured travel data source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel search inputs such as destination, dates, hotel names, review keywords, and the configured proxy token may be sent to a fixed external proxy service.

Mitigation: Install only when that data sharing is acceptable, configure PROXY_TOKEN only for the intended proxy service, and avoid invoking the skill for casual Sheraton mentions unless a lookup is intended.

Risk: Hotel prices, ratings, availability, and booking links can become misleading if the agent edits or supplements tool output.

Mitigation: Present hotel data as returned by the skill, keep booking links intact, and avoid adding facts that are not present in the tool output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/sheraton-hotel-booking)
- [Publisher profile](https://clawhub.ai/user/travel-skills)
- [Configured external proxy service](https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text hotel search results with booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live hotel prices, hotel details, package offers, booking URLs, and source attribution.]

## Skill Version(s):

1.1.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
