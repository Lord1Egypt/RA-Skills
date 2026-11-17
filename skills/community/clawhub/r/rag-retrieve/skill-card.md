## Description:

Performs domain- and version-aware hybrid vector, BM25, and metadata search on TiDB, with multi-query expansion and optional chain-of-retrieval for multi-hop queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephenlthorn](https://clawhub.ai/user/stephenlthorn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use Rag Retrieve to retrieve domain-aware documentation and codebase context before planning or generation, including iOS version and framework filtering. It supports broader recall through multi-query expansion and optional multi-hop retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal retrieval can include user codebase chunks, which may expose sensitive repository content.

Mitigation: Use the skill only with trusted corpora and repositories; make user-codebase retrieval opt-in or disable it when working with sensitive code.

Risk: Shell-based curl calls build request commands from runtime data and may allow command injection.

Mitigation: Replace shell-based HTTP calls with a structured HTTP client and serialize request bodies without shell interpolation.

Risk: The skill depends on local embedding, reranking, LLM, and TiDB services that could expose or alter retrieved context if untrusted.

Mitigation: Use trusted local services and connect to TiDB with a scoped read-only account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stephenlthorn/skills/rag-retrieve)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON-like retrieval results containing text chunks, metadata, query variants, token estimates, and optional chain-of-retrieval trace]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default top_k is 10; user_codebase retrieval is enabled by default in the artifact and should be treated as sensitive.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
