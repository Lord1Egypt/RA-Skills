## Description:

Retrieve semantically relevant Xiaohongshu competitor-note chunks from a local RAG index built by xhs-knowledge-indexer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kekena1016](https://clawhub.ai/user/kekena1016)

### License/Terms of Use:

MIT-0

## Use Case:

Content strategists, planners, and writing agents use this skill to retrieve relevant Xiaohongshu competitor-note examples from a trusted local RAG index before planning or drafting content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local index and output paths are caller-controlled and may expose or overwrite data if pointed at untrusted locations.

Mitigation: Install and run the skill only with trusted XHS knowledge-index and output paths.

Risk: The sentence-transformers dependency can attempt a model download when the required embedding model is absent from the local cache.

Mitigation: Pre-cache the embedding model used by index.json when offline or controlled-network operation is required.

Risk: Retrieved competitor-note chunks may include third-party text that should not be republished verbatim.

Mitigation: Use retrieved chunks as inspiration and review generated content before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kekena1016/skills/xhs-knowledge-retriever)
- [Project homepage](https://github.com/catherinewu/xhs-knowledge-retriever)
- [Canonical Competitor RAG Storage](docs/KNOWLEDGE_CONTRACT.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON object containing the query, embedding model, top-k results, similarity scores, retrieved chunks, and source metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local XHS knowledge index; optional output path writes the same JSON to disk.]

## Skill Version(s):

0.1.0 (source: changelog, release metadata, and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
