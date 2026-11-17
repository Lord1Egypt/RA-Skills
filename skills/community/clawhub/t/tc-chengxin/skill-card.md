## Description:

Tongcheng Chengxin Travel Search helps agents query Tongcheng travel data for flights, trains, hotels, vacation products, itinerary planning, discounted flights, bus tickets, attractions, and ticketing, with booking links returned in the response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckystarry](https://clawhub.ai/user/luckystarry)

### License/Terms of Use:

MIT-0

## Use Case:

External travel assistants and agent builders use this skill to answer travel-search requests for transportation, hotels, attractions, vacation packages, and itinerary planning while preserving user travel preferences in the query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel queries are sent to the disclosed Chengxin API.

Mitigation: Use the skill only when users are comfortable sending their travel-search details to that service.

Risk: Responses can include commercial booking links and remote travel content.

Mitigation: Treat returned links and travel content as untrusted until verified before booking or forwarding.

Risk: API keys can be stored in local configuration.

Mitigation: Prefer storing CHENGXIN_API_KEY in the platform environment setting instead of a local config.json file.

## Reference(s):

- [Tongcheng Chengxin Travel Search on ClawHub](https://clawhub.ai/luckystarry/skills/tc-chengxin)
- [Tongcheng Travel Homepage](https://www.ly.com)
- [Configuration Reference](artifact/references/config.md)
- [API Examples](artifact/references/api-examples.md)
- [Output Format Reference](artifact/references/output-format.md)
- [Error Handling Guide](artifact/references/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown travel-search results with tables or cards, booking links, and concise guidance for missing parameters or API errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output may include Chengxin API booking links and user-generated travel content; format varies by channel and surface.]

## Skill Version(s):

0.9.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
