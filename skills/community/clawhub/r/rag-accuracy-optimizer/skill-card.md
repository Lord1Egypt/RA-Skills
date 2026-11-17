## Description:

Optimize accuracy for RAG systems through data design, chunking, retrieval tuning, evaluation, monitoring, and anti-hallucination safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddieluong](https://clawhub.ai/user/eddieluong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, tune, evaluate, and monitor RAG pipelines for higher retrieval and answer accuracy across domains such as insurance, finance, healthcare, e-commerce, and Vietnamese-language applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples and scripts may send documents, embeddings, questions, answers, or retrieved contexts to cloud AI providers.

Mitigation: Prefer local models by default, require explicit opt-in for cloud providers, and redact or minimize sensitive fields before any external request.

Risk: RAG query logs and monitoring records may persist raw user queries, retrieved chunks, answers, and feedback.

Mitigation: Apply retention limits, access controls, and redaction for logs before using the skill with private or regulated data.

Risk: Dependency installation examples do not provide pinned versions or hash-verified lock files.

Mitigation: Pin dependencies with hashes or use a reviewed lock file before production or private-data use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/eddieluong/skills/rag-accuracy-optimizer)
- [Chunking Patterns](references/chunking-patterns.md)
- [Retrieval Patterns](references/retrieval-patterns.md)
- [Embedding Models](references/embedding-models.md)
- [Vector Database Comparison](references/vector-db-comparison.md)
- [Advanced RAG Techniques](references/advanced-rag.md)
- [RAG Testing and Evaluation Frameworks](references/testing-frameworks.md)
- [Vietnamese NLP Processing for RAG](references/vietnam-nlp.md)
- [Orchestrator Patterns](references/orchestrator-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; bundled scripts can emit JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional evaluation, chunk-quality, and embedding-benchmark scripts; cloud provider examples require explicit user-supplied credentials.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
