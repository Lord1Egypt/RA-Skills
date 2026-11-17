## Description:

Execute Retrieval-Augmented Generation (RAG) using Ragie.ai for document ingestion, retrieval, document management, and grounded answer construction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hatim-be](https://clawhub.ai/user/hatim-be)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to upload documents or URLs to Ragie.ai, retrieve relevant chunks from a knowledge base, manage stored documents, and produce grounded answers with document citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents, URLs, queries, filters, and metadata are processed by Ragie.ai.

Mitigation: Use the skill only for content intended for Ragie.ai processing and scope retrieval with partitions or filters when appropriate.

Risk: RAGIE_API_KEY provides access to the configured Ragie.ai account.

Mitigation: Keep the API key private, load it from environment variables, avoid committing .env files, and do not log sensitive headers.

Risk: Document management commands can delete stored Ragie.ai documents.

Mitigation: Review document IDs carefully before confirming deletion.

## Reference(s):

- [Ragie API base URL](https://api.ragie.ai)
- [Ragie application](https://app.ragie.ai)
- [ClawHub skill page](https://clawhub.ai/hatim-be/skills/ragie-rag)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown responses, JSON retrieval results, and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RAGIE_API_KEY and sends selected documents, URLs, queries, filters, and metadata to Ragie.ai.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
