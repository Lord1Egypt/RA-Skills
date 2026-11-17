## Description:

Use the shared Pinecone RAG index for workspace agents that need to ingest markdown or text documents into pulse-rag or query semantic context from the shared index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptobro-man](https://clawhub.ai/user/cryptobro-man)

### License/Terms of Use:


## Use Case:

Developers and workspace agents use this skill to ingest approved markdown or text documents into a shared Pinecone RAG index and query semantic context from the default namespace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared ingestion and query access can expose documents placed in the shared Pinecone index to other agents using the default namespace.

Mitigation: Only ingest non-sensitive documents approved for shared workspace retrieval, and confirm who can query the default namespace before use.

Risk: The skill executes mutable external local code from the rag-pinecone-starter project and its Python virtual environment.

Mitigation: Verify the external project and .venv are trusted, current, and protected from unapproved modification before running the scripts.

Risk: The workflow depends on a Pinecone API key configured outside the skill.

Mitigation: Store PINECONE_API_KEY in the referenced environment file with appropriate access controls and rotate it if workspace exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptobro-man/skills/shared-pinecone-rag)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an existing rag-pinecone-starter project, protected Python virtual environment, and PINECONE_API_KEY configured outside the skill.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
