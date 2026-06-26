## Description: <br>
Build pipelines, agents, RAG flows, and full web services by combining Upstage Solar models, embeddings, document processing APIs, and deployment workflow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upstage-deployment](https://clawhub.ai/user/upstage-deployment) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build Upstage-based applications, RAG pipelines, document processing workflows, and deployable web services. It helps select Solar models, generate API code, scaffold projects, configure environment variables, and return deployment details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected prompts and documents to Upstage APIs, including potentially sensitive or regulated content. <br>
Mitigation: Use it only with approved data, confirm Upstage processing and retention requirements, and avoid submitting confidential or personal documents unless authorized. <br>
Risk: The skill requires an Upstage API key and can drive API usage that may incur cost. <br>
Mitigation: Use a dedicated API key with least privilege, spending limits, and rotation practices; never hardcode or log the key. <br>
Risk: The skill can scaffold and deploy web applications, creating external exposure if configured publicly. <br>
Mitigation: Confirm before external deployment, prefer private or password-protected delivery, and review generated application code and environment configuration before release. <br>
Risk: Generated reasoning or intermediate fields may expose raw model outputs or sensitive context if logged or returned directly. <br>
Mitigation: Do not expose or log raw reasoning fields in production, and sanitize generated outputs before sharing them with users or downstream systems. <br>


## Reference(s): <br>
- [Upstage API Docs for Agents](https://console.upstage.ai/api/docs/for-agents/raw) <br>
- [Upstage Console](https://console.upstage.ai) <br>
- [Upstage Studio](https://studio.upstage.ai) <br>
- [Chat Completions API](artifact/references/chat-completions.md) <br>
- [Embeddings API](artifact/references/embeddings.md) <br>
- [Document Processing APIs](artifact/references/document-processing.md) <br>
- [Information Extraction API](artifact/references/information-extraction.md) <br>
- [Document Classification API](artifact/references/document-classification.md) <br>
- [Agent API](artifact/references/agent-api.md) <br>
- [Common Patterns, Errors, and Limits](artifact/references/common-patterns.md) <br>
- [Webapp Project and Deployment Workflow](artifact/references/webapp-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Markdown, Files] <br>
**Output Format:** [Markdown with code blocks, configuration snippets, file paths, and deployment instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce application scaffolds, environment variable instructions, generated API examples, and document workflow outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
