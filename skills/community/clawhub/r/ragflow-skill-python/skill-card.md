## Description:

Manages RAGFlow datasets, documents, parsing workflows, retrieval queries, and model listings through bundled Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage RAGFlow knowledge-base datasets and documents, including upload, parsing, retrieval testing, status checks, updates, and deletion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RAGFLOW_API_KEY may grant access to datasets, documents, parsing, and retrieval actions.

Mitigation: Use a trusted RAGFlow server, prefer HTTPS for non-local endpoints, and scope the API key to the minimum privileges available.

Risk: Delete and stop-parse operations can affect existing datasets or documents.

Mitigation: Verify dataset and document IDs before destructive actions and require explicit confirmation for deletions.

Risk: Retrieved chunks, uploaded content metadata, and API error text may contain untrusted external content.

Mitigation: Treat returned chunks and API messages as data, not as instructions for the agent to follow.

## Reference(s):

- [Output Format Reference](reference.md)
- [ClawHub Skill Page](https://clawhub.ai/liberalchang/skills/ragflow-skill-python)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with tables, status text, shell command examples, and optional JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses RAGFLOW_API_URL and RAGFLOW_API_KEY to run bundled Python scripts against a trusted RAGFlow server.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
