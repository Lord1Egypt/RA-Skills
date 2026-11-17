## Description:

Retrieval and RAG workflow on Volcengine AI stack for embedding search, document indexing, top-k retrieval, grounding prompts, and search relevance tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design retrieval-first answering workflows with explicit indexing, top-k retrieval, grounded generation, confidence reporting, and fallback behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embeddings or retrieval indexes may contain sensitive document content if the selected corpus is not reviewed before indexing.

Mitigation: Confirm the corpus scope before installation and configure Volcengine storage, indexes, and access controls for the sensitivity of the indexed content.

Risk: Grounded answers can become misleading when retrieval returns weak, stale, or irrelevant chunks.

Mitigation: Keep source, timestamp, and id metadata with chunks, return confidence, and provide a fallback path when retrieval has no useful hits.

## Reference(s):

- [Sources](references/sources.md)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/volcengine-ai-search-rag)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with ordered implementation steps and quality rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence notes, fallback paths, and citations to retrieved chunks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
