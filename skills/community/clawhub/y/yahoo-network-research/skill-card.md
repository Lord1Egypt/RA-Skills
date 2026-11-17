## Description:

Retrieves Yahoo editorial stories, full articles, comments, shopping deals and lists, and sports data across Autos, Entertainment, Health, Life, News, Shopping, Sports, and Tech, returning normalized JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve Yahoo editorial stories and full articles, read Yahoo News comments, find Yahoo Shopping deals and lists, and look up Yahoo Sports scores, standings, schedules, and related public data. The skill returns normalized JSON for use in research and answers about Yahoo's editorial network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill requires sending a Crawlora API key with requests to that service.

Mitigation: Confirm you trust Crawlora before use, and provide the key through CRAWLORA_API_KEY as documented rather than hardcoding or committing it.

Risk: The security review is incomplete because two local path references could not be resolved.

Mitigation: Review the release package and confirm the referenced paths before installation.

## Reference(s):

- [Yahoo Network Research on ClawHub](https://clawhub.ai/crawlora-org/skills/yahoo-network-research)
- [Yahoo endpoint reference](artifact/reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [JSON, Research data]

**Output Format:** [Normalized JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Yahoo editorial content and sports data; available snapshots and filters vary by endpoint.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
