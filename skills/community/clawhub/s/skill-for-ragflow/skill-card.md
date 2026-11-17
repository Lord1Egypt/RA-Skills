## Description:

Operate RAGFlow v0.27.3 deployments through a bundled Node CLI for everyday knowledge-base setup, document ingestion, parsing, retrieval, chat assistants, agents, GraphRAG, connectors, models, embedded website access, system-token listing/creation/deletion, and diagnostics. Use when a request explicitly involves a RAGFlow server, dataset, document pipeline, or RAGFlow agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunarcache](https://clawhub.ai/user/lunarcache)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and RAGFlow administrators use this skill to manage datasets, documents, retrieval, chat and agent workflows, connectors, models, and embedded access on an authorized RAGFlow deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says runtime permissions are unknown and the scan was partial, so some component behavior may not have been fully assessed.

Mitigation: Verify the host's runtime permissions and review the complete skill package before use; limit credentials and execution to the authorized RAGFlow deployment.

Risk: The skill can modify tenant data and manage system tokens, including destructive operations.

Mitigation: Confirm the exact target and authorized scope before destructive changes, use the CLI's explicit destructive confirmation, and protect a dedicated, rotatable API key.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lunarcache/skills/skill-for-ragflow)
- [Project homepage](https://github.com/LunarCache/ragflow-skill)
- [Command reference](references/COMMANDS.md)
- [Agent guide](references/AGENT_GUIDE.md)
- [Troubleshooting guide](references/TROUBLESHOOTING.md)
- [Programmatic API reference](references/API.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [JSON and human-readable command results, with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include status labels, retrieved content, and files downloaded to a requested path.]

## Skill Version(s):

5.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
