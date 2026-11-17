## Description:

Sovereign AI knowledge infrastructure with a typed entity graph, documents, long-term memory, messaging relay, and AI governance backed by PostgreSQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoinesrvt](https://clawhub.ai/user/antoinesrvt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Synap to store, search, update, and relate persistent knowledge in a configured Synap pod. It supports memory, documents, typed entities, relations, and external message relay with governance controls for writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can store facts, documents, relationships, and relayed channel messages in the configured Synap pod.

Mitigation: Use a Synap pod whose storage and privacy expectations are acceptable for the data being handled.

Risk: The skill requires write authority for its intended memory, document, entity, relation, and relay workflows.

Mitigation: Use least-privilege API keys where available and configure governance so important business data changes require review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/antoinesrvt/skills/synap)
- [Synap OpenClaw](https://synap.live/openclaw)
- [Synap](https://synap.live)
- [Hub Protocol](https://synap.live/docs/hub-protocol)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON request bodies, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Synap Hub API key and a configured Synap pod URL.]

## Skill Version(s):

1.0.0 (source: server evidence release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
