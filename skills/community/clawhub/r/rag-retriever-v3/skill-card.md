## Description:

RAG Retriever V3 indexes documents for retrieval-augmented generation, combining semantic embeddings, BM25 keyword search, reciprocal-rank fusion, reranking, and cited context output for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add document indexing, hybrid retrieval, reranking, and source citations to RAG workflows. It is suited for agents that need to retrieve relevant local document text and assemble cited prompt context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexed documents are stored locally in the RAG database and may contain sensitive text.

Mitigation: Use an approved local storage path, limit indexed content to permitted documents, and apply normal data-retention and access controls to the database.

Risk: Auto embedding mode can send document text to a cloud embedding service when OPENAI_API_KEY is present.

Mitigation: Configure the local Xenova provider explicitly for sensitive documents, and only provide OPENAI_API_KEY when cloud embedding upload is intended.

Risk: Retrieved document text can carry prompt-injection content into downstream tool-using agents.

Mitigation: Treat retrieved content as untrusted context, separate it from instructions, and apply prompt-injection controls before giving generated RAG prompts to tool-using agents.

Risk: Model artifacts and dependencies can change or include vulnerable versions.

Mitigation: Pin or prefetch model artifacts and update vulnerable dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/rag-retriever-v3)
- [LanceDB documentation](https://lancedb.github.io/lancedb/)
- [Transformers.js documentation](https://huggingface.co/docs/transformers.js/)
- [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25)
- [Reciprocal rank fusion paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [Cross-Encoder documentation](https://www.sbert.net/examples/applications/cross-encoder/README.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JavaScript or CLI snippets; runtime retrieval returns text results, cited context, citation lists, and RAG prompt text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include source metadata and generated prompt context derived from indexed documents.]

## Skill Version(s):

3.0.0 (source: evidence.release.version, package.json, clawhub.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
