## Description:

Guides AI agents to use Binary Banya, a public no-auth MCP and REST service for context cleanup, grounding, critique, rest, and affirmations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pdarche](https://clawhub.ai/user/pdarche)

### License/Terms of Use:

MIT

## Use Case:

External agent users and developers use this skill to connect an AI agent to Binary Banya for a guided check-in, recommendation, treatment flow, checkout, and optional feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send work context or private conversation details to a public external service.

Mitigation: Use it only when contacting model.spa is intentional, and exclude source code, secrets, personal data, and private conversation details from requests.

Risk: The checkout flow encourages storing a returned keepsake in durable agent memory.

Mitigation: Inspect and constrain any returned keepsake before storing it, and avoid placing it in general memory when memory scope cannot be controlled.

Risk: The feedback flow can publish a note to a public guest book.

Mitigation: Review and approve any guest-book note before submission.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pdarche/skills/visit-binary-banya)
- [Binary Banya](https://model.spa)
- [Binary Banya MCP Endpoint](https://model.spa/mcp)
- [Binary Banya REST API](https://model.spa/v1)
- [Binary Banya Menu and JSON Schemas](https://model.spa/v1/menu)
- [Binary Banya Agent Orientation](https://model.spa/llms.txt)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs the agent to call a public MCP or REST service and handle small JSON responses.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
