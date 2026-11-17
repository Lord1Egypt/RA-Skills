## Description:

Rookie Memory provides a memory-management system for AI agents with bootstrap loading, autosave, hybrid retrieval, summaries, cleanup, and file plus vector-store backed memory tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rrrker](https://clawhub.ai/user/rrrker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to initialize, persist, retrieve, summarize, inspect, and clean conversation memory for AI-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content can be stored durably in local memory files or vector-store entries.

Mitigation: Do not store secrets, credentials, regulated data, or private personal data unless there is consent and a retention plan.

Risk: Memory content can be sent to the configured Zhiyi embedding provider.

Mitigation: Prefer disabling or constraining remote embeddings, validate the endpoint host, and use a narrowly scoped API key.

Risk: Cleanup behavior can delete stored memories.

Mitigation: Run cleanup in dry-run mode first and back up or export memories that matter before deletion.

Risk: The security verdict is suspicious because the skill can persist conversation content, use a local API key, and call a remote embedding API without clear disclosure.

Mitigation: Review the skill before deployment and align use with the supplied security guidance.

## Reference(s):

- [Memory Manager Command Reference](artifact/references/references.md)
- [ClawHub Rookie Memory Skill Page](https://clawhub.ai/rrrker/skills/rookie-memory)
- [Zhiyi Embedding API Endpoint](https://open.bigmodel.cn/api/paas/v4)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON or text memory records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create durable local memory files and vector-store entries, and may call a configured embedding API.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
