## Description: <br>
Local vector knowledge base with GraphRAG retrieval that lets agents store private notes or documents and retrieve relevant context using vector, BM25, and knowledge-graph signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[er6y](https://clawhub.ai/user/er6y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to build, append, and query a local private knowledge base from documents or short notes. It is suited for KB-assisted answers where the agent retrieves context before composing a response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist user-provided documents, notes, and retrieved chunks in local knowledge-base storage. <br>
Mitigation: Avoid storing secrets, credentials, regulated data, or confidential documents unless the deployment owner has confirmed retention, access, and deletion behavior. <br>
Risk: Retrieved knowledge-base context may be sent to an external OpenAI-compatible LLM API when query generation is enabled. <br>
Mitigation: Use retrieval-only mode or a confirmed local endpoint for sensitive content, and review the configured API base URL and key handling before use. <br>
Risk: Background indexing can continue after a build command returns, so users may query a partially built knowledge base. <br>
Mitigation: Check build status before querying and communicate when indexing is still in progress. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/er6y/py-mnn-kb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Text or JSON results with retrieved context, status objects, shell commands, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Build commands may return immediately while indexing continues in the background; query output can include retrieved document context and optional generated answers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
