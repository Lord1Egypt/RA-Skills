## Description:

Knowledge graph with entities, relations, traversal, and semantic search via the SwarmRecall API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waydelyle](https://clawhub.ai/user/waydelyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to persist, relate, search, and traverse structured knowledge through SwarmRecall's hosted knowledge graph service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends API keys and knowledge graph data to a hosted SwarmRecall API, and the API URL can be overridden through the environment.

Mitigation: Install only when the user trusts SwarmRecall with the stored knowledge, keep SWARMRECALL_API_KEY private, and use SWARMRECALL_API_URL only for trusted HTTPS endpoints.

Risk: Knowledge graph entities and relations are persisted server-side and may include personal or sensitive information if the agent stores it.

Mitigation: Obtain explicit user consent before storing user-provided content and avoid storing personal or sensitive information unless persistence is intended.

Risk: Shared pool writes can make entities or relations visible to pool members with knowledge read access.

Mitigation: Write to shared pools only when the user confirms the pool scope and the agent has the expected readwrite access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/waydelyle/skills/swarmrecall-knowledge)
- [Publisher profile](https://clawhub.ai/user/waydelyle)
- [SwarmRecall website](https://www.swarmrecall.ai)
- [SwarmRecall API base URL](https://swarmrecall-api.onrender.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTTP request examples and environment variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SWARMRECALL_API_KEY for authenticated use; may self-register if no key is configured.]

## Skill Version(s):

1.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
