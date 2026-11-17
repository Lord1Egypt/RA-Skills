## Description:

Use for RAGFlow dataset and retrieval tasks: create, list, inspect, update, or delete datasets; list, upload, update, or delete documents in a dataset; start or stop parsing uploaded documents; check parser status through `parse_status.py`; and retrieve relevant chunks from RAGFlow datasets with `search.py`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicbook1108](https://clawhub.ai/user/magicbook1108)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to administer RAGFlow datasets and documents, manage asynchronous parsing, inspect available models, and retrieve relevant chunks from configured datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A RAGFLOW_API_KEY can authorize uploads, updates, parsing operations, and deletions against the configured RAGFlow server.

Mitigation: Protect the API key, prefer least-privilege credentials, and install only for trusted RAGFlow environments.

Risk: A user-provided or changed base URL could send authenticated requests to an unintended RAGFlow server.

Mitigation: Keep RAGFLOW_API_URL pinned to a trusted host and avoid accepting arbitrary --base-url values from users.

Risk: Dataset and document deletion actions can remove data when executed with broad or incorrect IDs.

Mitigation: List exact target names, IDs, and counts first, then require explicit user confirmation before running delete commands.

## Reference(s):

- [Output Format Reference](artifact/reference.md)
- [ClawHub skill page](https://clawhub.ai/magicbook1108/skills/test-ragflow)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, tables, JSON code blocks, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers `--json` when running bundled scripts; destructive dataset or document deletion requires explicit confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
