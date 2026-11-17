## Description:

Maintains a local directory-based knowledge base using Python, FAISS, BM25, Alibaba Bailian text-embedding-v4 embeddings, and optional qwen3-rerank for hybrid, semantic, and keyword retrieval over prepared OpenClaw text assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadbbz](https://clawhub.ai/user/kadbbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain local document knowledge bases after OpenClaw has extracted source files into text, summaries, chunks, and T2Q prompts. It supports indexing, rebuilding, deletion, protected-term updates, and hybrid, semantic, or keyword retrieval across one or more knowledge bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted or untrusted knowledge-base files could cause unintended local files to be indexed and sent to the disclosed external embedding service.

Mitigation: Install only where knowledge-base directories are writable by trusted users; reject symlinks and enforce resolved-path containment before production use.

Risk: Sensitive or regulated document text may be sent to Alibaba DashScope during embedding or reranking.

Mitigation: Avoid indexing sensitive or regulated files unless external processing through Alibaba DashScope has been approved.

Risk: Delete operations alter local knowledge-base index artifacts and can remove document entries.

Mitigation: Add explicit warnings or confirmations for delete operations in production workflows.

Risk: Unpinned Python dependencies may change behavior over time.

Mitigation: Pin dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kadbbz/skills/rag-kb)
- [Path and naming rules](references/layout.md)
- [Content format rules](references/content-rules.md)
- [Runtime notes](references/runtime-notes.md)
- [DashScope embeddings endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings)
- [DashScope rerank endpoint](https://dashscope.aliyuncs.com/compatible-api/v1/reranks)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown query results, command examples, configuration guidance, and local index artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results return real chunks grouped by source document; semantic and hybrid modes require external embedding calls, and reranking requires an external rerank call.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
