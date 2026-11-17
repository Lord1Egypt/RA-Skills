## Description:

Builds and searches lightweight TurboVec document indexes for semantic and hybrid retrieval on resource-constrained hardware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rochyroch](https://clawhub.ai/user/rochyroch)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and engineers use this skill to build compact searchable indexes from Markdown or text document collections and run semantic, hybrid, or reranked search for RAG workflows on limited hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexes from untrusted sources may include unsafe BM25 serialized data.

Mitigation: Search only indexes you built or independently trust; remove bm25_index.pkl before searching third-party index directories.

Risk: Document text is sent to the configured embedding endpoint and stored in generated chunks.json files.

Mitigation: Use a trusted local Ollama endpoint for sensitive documents and protect generated index directories.

Risk: Quantized search can change result ranking and is not suited to critical recall-sensitive medical, legal, or financial use cases.

Mitigation: Use a higher-recall retrieval stack and validate with known queries before relying on results in critical workflows.

## Reference(s):

- [TurboVec Quantization Explained](references/quantization.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with inline shell commands, generated index files, and optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include source filenames, text chunks, relevance scores, timing, and expanded context.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
