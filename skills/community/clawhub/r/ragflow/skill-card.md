## Description:

Universal Ragflow API client for RAG operations. Create datasets, upload documents, run chat queries against knowledge bases. Self-hosted RAG platform integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angusthefuzz](https://clawhub.ai/user/angusthefuzz)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to manage Ragflow datasets, upload documents, trigger parsing, and run RAG chat queries against self-hosted knowledge bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can delete knowledge bases without an interactive confirmation step.

Mitigation: Manually confirm dataset IDs before running delete-dataset and use an API key limited to the datasets the agent should manage.

Risk: API keys and uploaded documents may be sent over unencrypted HTTP if RAGFLOW_URL is configured that way.

Mitigation: Use HTTPS for RAGFLOW_URL and connect only to Ragflow servers the operator trusts.

Risk: Document upload sends selected local file contents to the configured Ragflow server.

Mitigation: Upload only intended files and avoid sensitive local documents unless their transfer is authorized.

## Reference(s):

- [Ragflow API docs](https://ragflow.io/docs)
- [ClawHub skill page](https://clawhub.ai/angusthefuzz/skills/ragflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JavaScript examples, and API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus RAGFLOW_URL and RAGFLOW_API_KEY environment variables.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
