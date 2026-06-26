## Description: <br>
Vector DB Toolkit provides vector database operations for AI/RAG applications across Qdrant, Chroma, and in-memory vector stores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create collections, upsert vectors and payloads, run semantic similarity search, and manage vector data in RAG workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vector database delete operations can remove points or entire collections when called with the wrong collection name or identifier. <br>
Mitigation: Use test collections first and verify collection names and point IDs before running delete calls. <br>
Risk: Persistent Chroma storage can write vector data and payload metadata to disk at the configured path. <br>
Mitigation: Choose an intentional Chroma storage path and apply normal data handling controls for stored embeddings and metadata. <br>
Risk: The optional OpenAI embedding provider sends input text to OpenAI using the configured API key. <br>
Mitigation: Do not use provider='openai' with confidential text unless that transfer is acceptable under the user's API key and data policy. <br>
Risk: Unpinned dependency ranges can change installed package versions over time. <br>
Mitigation: For production use, install with pinned and scanned dependencies. <br>


## Reference(s): <br>
- [Qdrant API Patterns](references/qdrant_api.md) <br>
- [Chroma API Patterns](references/chroma_api.md) <br>
- [ClawHub release page](https://clawhub.ai/kaiyuelv/vector-db-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/kaiyuelv) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include vector database operations, embedding helper usage, dependency installation steps, and backend-specific configuration notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
