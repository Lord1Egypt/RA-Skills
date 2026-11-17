## Description:

Smart Memory System helps OpenClaw agents retrieve, organize, and inject relevant memories using semantic search and retrieval-augmented context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jazzqi](https://clawhub.ai/user/jazzqi)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to build an agent memory layer that indexes approved conversation history or documents, retrieves relevant items semantically, and injects compact context into future interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation history or selected documents may be persisted and automatically reused from local memory indexes.

Mitigation: Index only approved content and avoid secrets, credentials, regulated data, or confidential business documents unless retention, deletion, and backup behavior are clearly governed.

Risk: Indexed content may be processed by configured embedding or reranker providers.

Mitigation: Confirm provider privacy terms and data handling before enabling auto-enhancement, batch processing, or document indexing.

Risk: Install and maintenance disclosures are weak for dependency pinning, lockfiles, hooks, auto-enhancement, cleanup, export, and deletion controls.

Mitigation: Review dependencies, lockfiles, install hooks, and operational controls before deployment; prefer exact dependency pins and reviewable install behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jazzqi/skills/smart-memory-system)
- [Publisher profile](https://clawhub.ai/user/jazzqi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, JSON configuration, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initialize local memory indexes, semantic caches, topic clusters, backups, logs, and configuration under ~/.openclaw.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
