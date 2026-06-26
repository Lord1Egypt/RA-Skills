## Description: <br>
Use the shared Pinecone RAG index for any agent in this workspace. Use when an agent needs to ingest markdown/text docs into pulse-rag or query semantic context from the shared index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptobro-man](https://clawhub.ai/user/cryptobro-man) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to ingest markdown or text documents into a shared Pinecone-backed RAG index and query semantic context from that shared memory layer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates ingest and query actions to a hardcoded external RAG project path. <br>
Mitigation: Install only when you control and trust the rag-pinecone-starter project at that path, and review the external ingest and query scripts before use. <br>
Risk: Shared RAG memory can retain or expose documents across agents if sensitive content is ingested without governance. <br>
Mitigation: Ingest only documents suitable for shared agent memory, and define namespace, deletion, and retention practices before operational use. <br>
Risk: The workflow depends on a Pinecone API key for external retrieval infrastructure. <br>
Mitigation: Use a least-privilege Pinecone key and manage it through the referenced project environment file rather than embedding credentials in skill files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and setup notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local rag-pinecone-starter project, Python virtual environment, and Pinecone API key configured outside the skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
