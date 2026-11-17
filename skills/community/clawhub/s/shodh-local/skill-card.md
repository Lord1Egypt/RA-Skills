## Description:

Shodh Local helps agents use a local offline Shodh-Memory server for persistent memory, semantic recall, GTD todos and projects, a knowledge graph, proactive context, and context summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doobidoo](https://clawhub.ai/user/doobidoo)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to give OpenClaw-style agents local offline memory, todo and project tracking, semantic recall, and proactive context during ongoing work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist and reuse personal context under broad memory and recall triggers.

Mitigation: Require explicit approval before storing or using recalled memories for important actions, and avoid storing secrets or sensitive personal data.

Risk: A hard-coded user namespace or shared identifiers can mix context between users or agents.

Mitigation: Configure unique per-user and per-agent IDs and scoped API keys before use.

Risk: Persistent local memory can influence future agent behavior with stale or incorrect context.

Mitigation: Review recalled memories before relying on them and regularly delete or update outdated memories, todos, and projects.

## Reference(s):

- [Shodh API Endpoints](artifact/reference/api.md)
- [OpenClaw Examples](artifact/reference/examples.md)
- [ClawHub skill page](https://clawhub.ai/doobidoo/skills/shodh-local)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local API endpoint guidance and persistent-memory operating practices.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact describes Shodh-Memory v0.1.74)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
