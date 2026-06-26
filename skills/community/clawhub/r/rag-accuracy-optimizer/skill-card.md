## Description: <br>
Optimize accuracy for RAG systems with guidance for data design, chunking, retrieval optimization, evaluation, monitoring, and anti-hallucination safeguards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddieluong](https://clawhub.ai/user/eddieluong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, tune, evaluate, and monitor Retrieval-Augmented Generation pipelines across domains such as insurance, finance, healthcare, e-commerce, and Vietnamese-language applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example workflows can send prompts, document chunks, or evaluation data to cloud AI providers. <br>
Mitigation: Use approved providers and controlled environments, and avoid customer, healthcare, financial, legal, or proprietary data unless the deployment has explicit approval. <br>
Risk: Example monitoring and evaluation flows can log raw queries, retrieved context, or answers locally. <br>
Mitigation: Redact sensitive fields or disable raw query and context logging before using the examples with sensitive deployments. <br>
Risk: Generated recommendations may affect retrieval quality, costs, latency, and answer accuracy. <br>
Mitigation: Validate changes against a representative test suite and review results before applying them to production RAG systems. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/eddieluong/rag-accuracy-optimizer) <br>
- [Advanced RAG Techniques](references/advanced-rag.md) <br>
- [Chunking Patterns - Python Code Examples](references/chunking-patterns.md) <br>
- [Embedding Models - Detailed Comparison](references/embedding-models.md) <br>
- [Orchestrator Patterns - Multi-Model Cost Optimization](references/orchestrator-patterns.md) <br>
- [Retrieval Patterns - Python Code Examples](references/retrieval-patterns.md) <br>
- [RAG Testing & Evaluation Frameworks](references/testing-frameworks.md) <br>
- [Vector Database - Detailed Comparison](references/vector-db-comparison.md) <br>
- [Vietnamese NLP Processing for RAG](references/vietnam-nlp.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON evaluation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional scripts for chunk quality analysis, embedding benchmarks, RAG accuracy testing, and RAGAS evaluation.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
