## Description:

Builds and searches lightweight TurboVec document indexes for RAG workflows that need a small memory footprint or semantic search on resource-constrained hardware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rochyroch](https://clawhub.ai/user/rochyroch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build quantized document indexes from Markdown or text files and search them with vector, hybrid BM25, and optional reranking modes. It is aimed at personal, team, offline, and resource-constrained RAG workflows rather than high-consequence recall-critical domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaged local Supabase instructions describe access to private conversations, contacts, and a service-role database credential.

Mitigation: Review before installing; remove or ignore the local Supabase instructions unless that access is intentional, and replace service-role access with scoped read-only credentials.

Risk: Generated indexes can retain document text and metadata in local files such as chunks.json.

Mitigation: Build indexes only from documents approved for this storage path, protect index directories, and avoid sharing generated indexes that contain sensitive source text.

Risk: Document text and search queries may be sent to the configured embedding endpoint.

Mitigation: Use a trusted local embedding endpoint for sensitive content and review any non-local API URL before building or searching.

Risk: Quantized search can trade accuracy for memory savings and may miss or reorder important results.

Mitigation: Validate recall with known queries, use higher bit widths or reranking where needed, and avoid relying on this skill for medical, legal, financial, or other recall-critical decisions.

## Reference(s):

- [TurboVec Quantization Explained](references/quantization.md)
- [ClawHub skill page](https://clawhub.ai/rochyroch/skills/the-librarian)
- [Publisher profile](https://clawhub.ai/user/rochyroch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands; generated index files; optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Build output includes TurboVec index files, document chunks, BM25 JSON data, and build statistics; search output can include scores, source filenames, excerpts, and expanded context.]

## Skill Version(s):

1.2.1 (source: ClawHub release evidence; artifact SKILL.md states 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
