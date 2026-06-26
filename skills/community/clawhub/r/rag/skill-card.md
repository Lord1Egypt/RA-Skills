## Description: <br>
Build, optimize, and debug RAG pipelines with chunking strategies, retrieval tuning, evaluation metrics, and production monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design, implement, evaluate, and operate retrieval-augmented generation systems. It helps choose RAG architecture patterns, tune retrieval behavior, debug quality issues, and apply security and compliance controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RAG systems can expose sensitive, unnecessary, or unauthorized document content through indexing or retrieval. <br>
Mitigation: Control which documents are indexed, avoid storing secrets or unnecessary personal data, enforce retrieval-time access controls, and review retention and deletion policies for embedding and vector database providers. <br>
Risk: Retrieved content can include adversarial instructions or low-quality context that affects generated answers. <br>
Mitigation: Treat retrieved text as untrusted context, keep prompt-injection mitigations in place, filter suspicious outputs, and evaluate retrieval quality before production use. <br>


## Reference(s): <br>
- [RAG Architecture](architecture.md) <br>
- [RAG Implementation Guide](implementation.md) <br>
- [RAG Evaluation & Debugging](evaluation.md) <br>
- [RAG Security & Privacy](security.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with code snippets and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include architecture recommendations, implementation patterns, evaluation metrics, debugging steps, and security checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
