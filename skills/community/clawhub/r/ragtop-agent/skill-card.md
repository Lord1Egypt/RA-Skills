## Description:

Ragtop Agent helps agents manage RAGTOP knowledge bases, list documents, and perform multi-step semantic retrieval for document-grounded analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qbs784](https://clawhub.ai/user/qbs784)

### License/Terms of Use:


## Use Case:

Developers and knowledge workers use this skill to query RAGTOP knowledge bases, narrow retrieval to relevant documents, and synthesize answers with source-document citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens and user queries may be sent to a RAGTOP endpoint over unencrypted HTTP.

Mitigation: Use a trusted HTTPS RAGTOP endpoint instead of the default HTTP endpoint before sending sensitive prompts or credentials.

Risk: The skill requires a RAGTOP API token for backend API calls.

Mitigation: Use a narrowly scoped token, store it in RAGTOP_API_TOKEN, and rotate it if exposure is suspected.

Risk: Retrieved knowledge-base content may be incomplete or insufficient for a deep research answer.

Mitigation: Require source-document citations and explicitly state when retrieval results are insufficient.

## Reference(s):

- [Agentic RAG Workflow Guidelines](references/workflow.md)
- [ClawHub skill page](https://clawhub.ai/qbs784/skills/ragtop-agent)
- [Publisher profile](https://clawhub.ai/user/qbs784)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline curl commands and source-cited analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RAGTOP_API_TOKEN and a trusted RAGTOP endpoint; default endpoint evidence uses unencrypted HTTP.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
