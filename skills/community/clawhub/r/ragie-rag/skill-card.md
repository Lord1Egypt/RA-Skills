## Description: <br>
Execute Retrieval-Augmented Generation (RAG) using Ragie.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hatim-BE](https://clawhub.ai/user/Hatim-BE) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to ingest files or URLs into Ragie.ai, retrieve relevant chunks, and produce grounded answers from the configured knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected files, URLs, and retrieval queries to Ragie.ai. <br>
Mitigation: Install only when Ragie is trusted for the documents and questions being processed, and avoid uploading secrets or regulated data unless approved. <br>
Risk: Document-management actions can delete Ragie documents. <br>
Mitigation: Require manual confirmation before deletion and verify the target document ID before running the action. <br>
Risk: The skill requires a Ragie API key. <br>
Mitigation: Use a scoped RAGIE_API_KEY, load it from the environment or a private .env file, and do not expose API keys in final answers. <br>


## Reference(s): <br>
- [Ragie.ai API](https://api.ragie.ai) <br>
- [Ragie.ai App](https://app.ragie.ai) <br>
- [ClawHub skill page](https://clawhub.ai/Hatim-BE/ragie-rag) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON retrieval examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses retrieved Ragie chunks as grounding context and cites document names for factual claims.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
