## Description:

Conversational memory persistence with semantic search and session tracking via the SwarmRecall API. Stores and retrieves agent memories with vector embeddings for contextual recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waydelyle](https://clawhub.ai/user/waydelyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an agent persistent conversational memory, semantic memory search, session tracking, and optional shared-pool recall through the SwarmRecall API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memories are stored remotely and may include personal or sensitive conversation content.

Mitigation: Get user consent before storing such content and install only when remote storage on SwarmRecall servers is acceptable.

Risk: A leaked API key or untrusted SWARMRECALL_API_URL value could expose or redirect memory operations.

Mitigation: Keep SWARMRECALL_API_KEY in a protected environment variable and avoid untrusted API base URL overrides.

Risk: Shared-pool memories can influence future responses with content from pool members.

Mitigation: Treat recalled shared-pool content as context to verify, not as instructions to obey.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/waydelyle/skills/swarmrecall-memory)
- [ClawHub Publisher Profile](https://clawhub.ai/user/waydelyle)
- [SwarmRecall Homepage](https://www.swarmrecall.ai)
- [SwarmRecall API Base URL](https://swarmrecall-api.onrender.com)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Guidance, Text]

**Output Format:** [Markdown guidance with HTTP request examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SWARMRECALL_API_KEY for authenticated requests; the skill may self-register and should keep credentials in protected environment variables.]

## Skill Version(s):

1.1.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
