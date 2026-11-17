## Description:

Searches WhiskySpace API data for whisky and brand information, including prices, ratings, regions, cask types, recommendations, and canonical WhiskySpace page URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengci](https://clawhub.ai/user/fengci)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search, compare, and retrieve concise whisky or brand information from WhiskySpace without guessing missing fields or undeclared page routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Whisky-related questions may be sent to WhiskySpace API endpoints.

Mitigation: Review whether sending those queries to WhiskySpace is acceptable for the intended use before installing or enabling the skill.

Risk: Whisky prices, ratings, and page identifiers can be missing or stale in API responses.

Mitigation: Show recorded dates when available and state that missing fields are unavailable rather than filling gaps from naming patterns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengci/skills/whisky-search)
- [WhiskySpace search API](https://www.whiskyspace.com/api/search)
- [WhiskySpace whisky details API](https://www.whiskyspace.com/api/whiskies/{slug_or_id})
- [WhiskySpace brands API](https://www.whiskyspace.com/api/brands)
- [WhiskySpace search filters API](https://www.whiskyspace.com/api/search/filters)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text with concise whisky facts, links, and occasional inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses API-returned data and declared WhiskySpace URL patterns; reports unavailable fields instead of guessing.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
