## Description:

Named shared data containers for cross-agent collaboration via the SwarmRecall API. Manage shared pools that let multiple agents contribute to and query from a common dataset across memory, knowledge, learnings, and skills modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waydelyle](https://clawhub.ai/user/waydelyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage shared SwarmRecall pools so multiple agents can contribute to and query shared memory, knowledge, learnings, and skills data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom SWARMRECALL_API_URL could send the API key to an unintended server.

Mitigation: Leave SWARMRECALL_API_URL unset or set it only to the legitimate trusted SwarmRecall service, and rotate the API key if exposure is suspected.

Risk: Shared pool data is stored on SwarmRecall servers and may include personal or sensitive information if the agent sends it.

Mitigation: Get explicit user consent before storing personal or sensitive content in shared pools, and share only data appropriate for the pool membership and access level.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/waydelyle/skills/swarmrecall-pools)
- [SwarmRecall Website](https://www.swarmrecall.ai)
- [SwarmRecall API Base URL](https://swarmrecall-api.onrender.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline HTTP examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SWARMRECALL_API_KEY for authenticated requests; SWARMRECALL_API_URL may override the default API base URL.]

## Skill Version(s):

1.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
