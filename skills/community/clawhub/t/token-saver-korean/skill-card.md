## Description:

Korean-first context database for AI agents that stores, searches, compresses, tiers, archives, and tags memories to reduce context token use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorongss](https://clawhub.ai/user/dorongss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a Korean-first memory and context database for AI agents, including memory storage, hybrid search, summarization, tiering, and OpenClaw-oriented workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved or queried memory can be sent to Fireworks when embeddings are enabled.

Mitigation: Use the skill only with data approved for that service, disable embeddings or withhold FIREWORKS_API_KEY when external embedding calls are not acceptable, and purge local memory and embedding files when no longer needed.

Risk: Unsafe path handling can write outside the intended storage directory.

Mitigation: Use a restricted storage directory and avoid untrusted URI or category inputs.

Risk: The bundled init_bora_context.py imports specific OpenClaw state files.

Mitigation: Do not run init_bora_context.py unless those files are intentionally being imported into local memory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dorongss/skills/token-saver-korean)
- [ClawHub Publisher Profile](https://clawhub.ai/user/dorongss)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Python snippets, shell commands, configuration examples, and JSON-compatible memory/search records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local memory, WAL, session-state, backup, and embedding files; can call Fireworks for embeddings when FIREWORKS_API_KEY is set.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
