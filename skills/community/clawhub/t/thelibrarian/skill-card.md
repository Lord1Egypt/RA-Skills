## Description: <br>
Build and search lightweight quantized document indexes with TurboVec for low-memory RAG and semantic search on resource-constrained hardware. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rochyroch](https://clawhub.ai/user/rochyroch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build local document indexes and search them for RAG or knowledge-base workflows on low-memory devices, small VMs, and edge hardware. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted index directories can include a bm25_index.pkl file that may execute code when loaded. <br>
Mitigation: Search only indexes built locally or from trusted sources; isolate and review any downloaded or shared index directory before use. <br>
Risk: Generated index folders can contain source document text and metadata. <br>
Mitigation: Protect index directories with the same access controls as the source documents and delete them when they are no longer needed. <br>
Risk: Quantized retrieval can swap result ordering and is not recommended by the artifact for medical, legal, or financial records. <br>
Mitigation: Validate recall with representative queries and use a higher-accuracy retrieval stack for critical domains. <br>


## Reference(s): <br>
- [TurboVec Quantization Explained](references/quantization.md) <br>
- [The Librarian on ClawHub](https://clawhub.ai/rochyroch/thelibrarian) <br>
- [RandTrad Consulting](https://www.randtradconsulting.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local quantized index files, document chunk JSON, statistics JSON, and an optional BM25 pickle file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
