## Description:

Manages RAGFlow datasets and documents, including creation, updates, upload, parsing, retrieval, and model listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage RAGFlow datasets, documents, parsing, retrieval, and configured models through bundled Python command-line scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and uploaded documents may be exposed if the skill is pointed at a plain HTTP RAGFlow server.

Mitigation: Use an HTTPS RAGFLOW_API_URL, install only for trusted RAGFlow servers, and prefer a dedicated least-privilege API key.

Risk: Dataset and document commands can modify or delete remote RAGFlow data.

Mitigation: Confirm exact dataset or document IDs before destructive operations and require explicit user confirmation for delete actions.

## Reference(s):

- [Output Format Reference](artifact/reference.md)
- [ClawHub Skill Page](https://clawhub.ai/liberalchang/skills/ragflow-skill-python0418)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional JSON code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers JSON output from bundled scripts and preserves API error fields exactly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
