## Description:

Local vector knowledge base with GraphRAG retrieval for storing notes and indexing private documents for agent-assisted retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[er6y](https://clawhub.ai/user/er6y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to build local knowledge bases from documents or notes and retrieve relevant context before answering questions. It is suited to private RAG workflows where selected local content is indexed into SQLite-backed storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent indexing can store selected files and notes in a local knowledge base.

Mitigation: Install only for content users are comfortable indexing, limit indexed directories to intended material, and separate sensitive projects into scoped knowledge bases.

Risk: Retrieved private knowledge-base excerpts may be sent to a remote OpenAI-compatible LLM provider when query generation is enabled.

Mitigation: Use --no-llm or remove llm_api.base_url unless remote LLM processing is explicitly intended for the indexed content.

Risk: Model and knowledge-base configuration can affect confidentiality and trust for sensitive data.

Mitigation: Use simple safe knowledge-base identifiers and prefer a pinned, verified local model before using the skill with confidential data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/er6y/skills/py-mnn-kb)
- [Declared source repository](https://github.com/er6y/py_mnn_kb)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text and JSON status payloads, with Markdown guidance and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieval output may contain excerpts from user-selected local knowledge bases; build operations can run in the background and should be checked with status output.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
