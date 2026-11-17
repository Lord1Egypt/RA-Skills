## Description:

Extends the agent's memory with semantic search capabilities using Retrieval-Augmented Generation (RAG) for enhanced contextual awareness and continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carlosdelfino](https://clawhub.ai/user/carlosdelfino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to index OpenClaw memory files and search past decisions, conversations, and contextual notes for continuity across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive agent memories, and its sanitizer may not remove all secrets or personal data before indexing.

Mitigation: Limit mounted workspaces and memory directories, review memory contents before indexing, and avoid shared cross-agent memory directories unless that sharing is intended.

Risk: Memory text can be sent to an environment-configurable HTTP embedding endpoint.

Mitigation: Use only a trusted, preferably local Ollama endpoint, and do not point OLLAMA_HOST at an untrusted or remote HTTP service for sensitive memories.

Risk: Container images and Python dependencies affect the runtime trusted computing base.

Mitigation: Pin or locally build the container and dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/carlosdelfino/skills/rapport-memories)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text, JSON metrics, and Markdown memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include matching memory content, source path, taxonomy, creation time, and similarity score when available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
