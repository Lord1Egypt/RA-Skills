## Description:

VyasaGraph gives agents persistent short-term and long-term memory through local session state, an embedded knowledge graph, semantic search, and graph relations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minopop](https://clawhub.ai/user/minopop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent memory to agents, including current-session state, permanent entities, relationships, and searchable project or error history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad persistent memory can store sensitive or unwanted personal, project, or conversation details across sessions.

Mitigation: Require explicit user approval for long-term writes, narrow the auto-recording rules, and avoid credentials, financial details, health records, and other sensitive data.

Risk: Optional semantic embeddings can send stored observations to OpenAI when OPENAI_API_KEY is configured.

Mitigation: Leave OPENAI_API_KEY unset for keyword search unless users accept embedding requests for stored observations.

Risk: Local memory files persist until they are cleared or deleted.

Mitigation: Document retention expectations and periodically clear SESSION-STATE.md or delete memory.db when durable memory is no longer needed.

## Reference(s):

- [VyasaGraph GitHub Repository](https://github.com/minopop/vyasagraph)
- [VyasaGraph npm Package](https://www.npmjs.com/package/vyasagraph)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update local memory files and optionally use OPENAI_API_KEY for semantic embeddings.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
