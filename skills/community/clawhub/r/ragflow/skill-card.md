## Description: <br>
Universal Ragflow API client for RAG operations, including dataset management, document upload, chat queries, and self-hosted knowledge-base integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angusthefuzz](https://clawhub.ai/user/angusthefuzz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to a trusted Ragflow instance so it can create and manage datasets, upload selected documents, trigger parsing, and run RAG chat queries against knowledge bases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload chosen local files and manage datasets on the configured Ragflow server. <br>
Mitigation: Use only an approved Ragflow instance, configure HTTPS, and provide a least-privilege API key scoped to the intended datasets. <br>
Risk: The delete-dataset command deletes when invoked and does not ask for confirmation. <br>
Mitigation: Review dataset IDs before deletion and avoid using credentials with production dataset deletion permissions unless that access is required. <br>
Risk: RAG queries and uploaded documents may contain sensitive information. <br>
Mitigation: Do not grant access to sensitive local files or production datasets unless the Ragflow server is approved for that data. <br>


## Reference(s): <br>
- [Ragflow API documentation](https://ragflow.io/docs) <br>
- [ClawHub skill page](https://clawhub.ai/angusthefuzz/ragflow) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/angusthefuzz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses RAGFLOW_URL and RAGFLOW_API_KEY to make Ragflow REST API requests through Node.js.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
