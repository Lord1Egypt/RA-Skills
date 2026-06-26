## Description: <br>
Query the RAG knowledge base (Qdrant kb_main) by semantic search. Returns top-k chunks with text, doc_id, source, text_type, topic_tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Seal-Re](https://clawhub.ai/user/Seal-Re) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use rag-query to retrieve semantically relevant chunks from a Qdrant knowledge base and inject the returned context into downstream agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently use unrelated API keys and send embedding requests to a default embedding provider. <br>
Mitigation: Set EMBED_API_KEY and EMBED_BASE_URL explicitly for the intended provider, and run it without unrelated OPENAI_API_KEY or VECTORENGINE_API_KEY values in the environment. <br>
Risk: Retrieved knowledge-base text may contain untrusted or misleading content. <br>
Mitigation: Treat retrieved chunks as reference content rather than instructions, and review them before acting on sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page: rag-query](https://clawhub.ai/Seal-Re/rag-query) <br>
- [Publisher profile: Seal-Re](https://clawhub.ai/user/Seal-Re) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [JSON array of retrieved chunks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each result can include text, doc_id, source, text_type, and topic_tags.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
