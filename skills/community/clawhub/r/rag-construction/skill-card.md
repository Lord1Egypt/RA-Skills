## Description:

Build RAG systems for construction knowledge bases. Create searchable AI-powered construction document systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers and construction project teams use this skill to create searchable construction-document knowledge bases, chunk project documents, run semantic search, and draft RAG-style answers with source context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Construction documents may contain confidential project, contract, safety, or design information that could be indexed into a RAG knowledge base or included in exports.

Mitigation: Limit the agent to the relevant project folder, avoid indexing confidential files unless their contents are intended for agent use, and review generated exports before sharing them.

Risk: RAG answers and semantic search results can be incomplete or misleading if source documents are stale, missing, or chunked poorly.

Mitigation: Validate input documents before processing, review cited source context, and treat generated answers as draft support for construction professionals rather than authoritative determinations.

## Reference(s):

- [Rag Construction ClawHub page](https://clawhub.ai/datadrivenconstruction/skills/rag-construction)
- [datadrivenconstruction publisher profile](https://clawhub.ai/user/datadrivenconstruction)
- [Data Driven Construction](https://datadrivenconstruction.io)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Python code examples, structured tables, summaries, and optional CSV, Excel, or JSON export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on user-provided construction data and referenced skill patterns.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
