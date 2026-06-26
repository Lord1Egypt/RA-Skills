## Description: <br>
Provides text embedding, persistent vector storage, and cosine-similarity semantic search with incremental indexing and pluggable backend support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whoisme007](https://clawhub.ai/user/whoisme007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add semantic memory search to agent systems by embedding memory text, storing vectors locally, and retrieving relevant memories by similarity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory text, embeddings, and metadata are persisted under the configured local database path. <br>
Mitigation: Use a trusted local path with appropriate file permissions and avoid storing sensitive memory data unless local persistence is acceptable. <br>
Risk: Stored vector and ID-map files are reloaded from disk using an unsafe serialization format. <br>
Mitigation: Do not import or share database, FAISS, or ID-map files from untrusted sources; regenerate indexes from trusted memory data when possible. <br>
Risk: Future Pinecone or Weaviate backends may move memory data to external storage. <br>
Mitigation: Review backend documentation, credentials, data retention, and privacy controls before enabling cloud vector storage. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/whoisme007/semantic-vector-store) <br>
- [Publisher profile](https://clawhub.ai/user/whoisme007) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with Python examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for embedding text, storing vectors, searching memories, configuring storage paths and models, and running maintenance commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
