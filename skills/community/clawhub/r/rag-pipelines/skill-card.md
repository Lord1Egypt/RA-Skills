## Description:

Deep RAG workflow - document ingestion, chunking, metadata, retrieval and reranking, grounding and citations, evaluation, and failure modes including hallucination and staleness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, debug, and review retrieval-augmented generation systems for internal documentation, support assistants, copilots, PDFs, HTML, and code repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or access-controlled document collections may be exposed if retrieval pipelines do not preserve source access controls.

Mitigation: Preserve ACL filtering and source auditability when applying the workflow to private corpora.

Risk: High-stakes RAG answers can still be incorrect, stale, or insufficiently grounded.

Mitigation: Use human review gates, citation audits, and production monitoring for high-stakes use cases.

## Reference(s):

- [Rag Pipelines on ClawHub](https://clawhub.ai/codekungfu/skills/rag-pipelines)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown guidance with checklists and structured workflow stages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not execute code or request credentials; intended as workflow guidance for an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
