## Description: <br>
Voyage AI CLI guides agents in using the vai CLI for Voyage AI embeddings, reranking, MongoDB Atlas Vector Search, model discovery, similarity checks, and batch ingestion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrlynn](https://clawhub.ai/user/mrlynn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to generate and manage embeddings, rerank search results, create Atlas vector search indexes, store vectors, run similarity search, and learn common retrieval workflows with the vai CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing a global CLI package can introduce supply-chain risk if the package or publisher is not the expected one. <br>
Mitigation: Verify the voyageai-cli npm package and publisher before installation. <br>
Risk: API keys and database credentials can be exposed if entered directly into shell history or shared logs. <br>
Mitigation: Use least-privilege Voyage AI and MongoDB credentials, and avoid placing real API keys directly in shell history. <br>
Risk: Store, ingest, index create, and index delete commands can modify Atlas data or search infrastructure. <br>
Mitigation: Test these commands on non-production databases before using them on production collections. <br>
Risk: Embedded or ingested documents may be processed by external services and stored in MongoDB Atlas. <br>
Mitigation: Do not embed or ingest sensitive documents unless that processing and storage is intended. <br>


## Reference(s): <br>
- [Voyage AI CLI Skill on ClawHub](https://clawhub.ai/mrlynn/voyageai-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/mrlynn) <br>
- [Author Website](https://mlynn.org) <br>
- [Model Catalog](references/models.md) <br>
- [Atlas Vector Search Integration Patterns](references/vector-search.md) <br>
- [MongoDB AI API](https://ai.mongodb.com/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI command examples, configuration notes, and reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that call external Voyage AI and MongoDB Atlas services; users must supply VOYAGE_API_KEY and, for Atlas operations, MONGODB_URI.] <br>

## Skill Version(s): <br>
1.4.0 (source: release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
