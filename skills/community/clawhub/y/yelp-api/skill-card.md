## Description:

A Yelp API alternative on fetcher.sh for searching local businesses, retrieving business details by ID or Yelp URL handle, and fetching business reviews through paid JSON HTTP endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fetcher-sh](https://clawhub.ai/user/fetcher-sh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to search Yelp-style local business data, retrieve business details, and fetch reviews without using the Yelp Fusion API approval flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search queries, location inputs, business identifiers, and review requests to a third-party service.

Mitigation: Use only when the user or deployment policy permits sharing those request details with fetcher.sh.

Risk: API use is paid through prepaid bearer-key credits or x402 pay-per-call payment, and the artifact notes that refunds are not provided on upstream failures.

Mitigation: Review fetcher.sh pricing and payment mechanics before enabling the skill, and avoid exposing credentials in shared logs or prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fetcher-sh/skills/yelp-api)
- [Server-resolved GitHub provenance](https://github.com/fetcher-sh/fetcher-skills/tree/main/skills/yelp)
- [Full agent setup](https://yelp.fetcher.sh/skill.md)
- [OpenAPI 3.1 contract](https://yelp.fetcher.sh/openapi.json)
- [Condensed catalog](https://yelp.fetcher.sh/llms.txt)
- [Yelp Fetcher site](https://yelp.fetcher.sh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash, JSON, and HTTP endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to call third-party paid JSON endpoints for local business search, details, and reviews.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
