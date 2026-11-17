## Description:

Curates enterprise knowledge-base content for RAG by cleaning text, deduplicating passages, applying tags, scoring quality, and producing versioned Markdown governance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge-base maintainers, and RAG operations teams use this skill to prepare user-provided documents for retrieval pipelines by cleaning, chunking, tagging, scoring, and summarizing ingestion readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated chunking, tags, quality scores, or ingestion recommendations may be incorrect or incomplete for sensitive enterprise knowledge bases.

Mitigation: Review the generated governance report and recommendations before connecting outputs to a production vector database pipeline.

Risk: Source documents may contain sensitive enterprise material.

Mitigation: Apply the organization's data handling controls before providing documents to the skill or downstream retrieval systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boboy-j/skills/rag-knowledge-curator)
- [Publisher profile](https://clawhub.ai/user/boboy-j)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown governance report with summary tables, chunk previews, metadata, quality scores, and optimization recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses raw_documents, chunk_strategy, and domain inputs; schema recommends limiting a single input to 5000 characters for quality.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
