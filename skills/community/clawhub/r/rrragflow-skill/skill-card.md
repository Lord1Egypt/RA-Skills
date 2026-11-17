## Description:

This skill helps agents manage RAGFlow datasets and documents, control parsing, check parse status, retrieve chunks, and list configured models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redredrrred](https://clawhub.ai/user/redredrrred)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a RAGFlow knowledge base from an agent, including dataset management, document upload and deletion, parsing control, parse-status inspection, retrieval, and model listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and uploaded documents may be sent to a non-HTTPS RAGFlow endpoint if the endpoint is configured that way.

Mitigation: Use only a trusted RAGFlow endpoint, prefer HTTPS for any non-local service, and use a narrowly scoped RAGFLOW_API_KEY.

Risk: Dataset and document update or delete commands execute API changes once called with explicit IDs.

Mitigation: List the exact target items first, confirm dataset or document IDs carefully, and require explicit user confirmation before destructive actions.

## Reference(s):

- [Output Format Reference](artifact/reference.md)
- [ClawHub Skill Page](https://clawhub.ai/redredrrred/skills/rrragflow-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional JSON code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus RAGFLOW_API_URL and RAGFLOW_API_KEY; JSON API fields should be preserved exactly when returned.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
