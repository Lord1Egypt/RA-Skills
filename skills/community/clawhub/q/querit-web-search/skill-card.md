## Description:

Advanced web search using the Querit API with support for site filtering, time ranges, geolocation, and language targeting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[murphyzzzzz](https://clawhub.ai/user/murphyzzzzz)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run real-time Querit web searches for current facts, news, and targeted results filtered by site, time range, geography, or language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and advanced JSON search payloads are sent to Querit.

Mitigation: Do not include passwords, tokens, private internal URLs, customer data, or other sensitive material in searches.

Risk: The skill requires a Querit API key to call the search service.

Mitigation: Provide QUERIT_API_KEY only in the runtime environment and install the skill only where use of Querit is approved.

## Reference(s):

- [Querit](https://querit.ai)
- [Querit POST API reference](https://www.querit.ai/en/docs/reference/post)
- [ClawHub skill page](https://clawhub.ai/murphyzzzzz/skills/querit-web-search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON search results or JSON error messages returned by a command-line Python script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and QUERIT_API_KEY; sends search queries and advanced JSON search payloads to Querit.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
