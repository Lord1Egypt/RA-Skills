## Description:

Use for RAGFlow dataset tasks: create, list, inspect, update, or delete datasets; upload, list, update, or delete documents; start or stop parsing; check parse status; retrieve chunks with search.py; and list configured models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingfeng](https://clawhub.ai/user/yingfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage RAGFlow knowledge bases, documents, parsing jobs, retrieval checks, and configured models from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a RAGFlow API key against the server configured in RAGFLOW_API_URL.

Mitigation: Install only for trusted RAGFlow servers, prefer HTTPS for remote servers, and use least-privilege API keys where possible.

Risk: Dataset and document update or delete actions can modify or remove RAGFlow content.

Mitigation: Review destructive actions carefully, list exact target items first, and proceed only with explicit dataset or document IDs after user confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yingfeng/skills/ragflow-skill)
- [Publisher Profile](https://clawhub.ai/user/yingfeng)
- [Output Format Reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, tables, JSON code blocks, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relays RAGFlow API fields exactly when JSON output is used; requires RAGFLOW_API_URL, RAGFLOW_API_KEY, and python3.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
