## Description:

Searches Ritz-Carlton hotels in Marriott-related inventory and returns live prices, hotel details, package offers, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to find Ritz-Carlton hotel availability, prices, details, packages, and booking links for a requested destination or hotel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel search terms, destinations, dates, hotel names, and optional review keywords are sent to an external proxy service for live results.

Mitigation: Install and use the skill only where sharing those travel query details with the configured proxy is acceptable.

Risk: The trigger term can be ambiguous when the user only says "丽思".

Mitigation: Confirm ambiguous prompts before invoking hotel search, detail, or package lookup commands.

Risk: Hotel names, prices, ratings, policies, and booking links can be misleading if the agent supplements or edits script output.

Mitigation: Present only values returned by the tool output and avoid adding unsourced hotel facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/ritz-carlton-hotel-booking)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with booking links and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns hotel search results, hotel details, or package offers from the configured live data proxy.]

## Skill Version(s):

1.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
