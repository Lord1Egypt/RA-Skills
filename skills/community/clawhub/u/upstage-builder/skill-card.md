## Description:

Build pipelines, agents, RAG flows, and full web services by combining Upstage Solar models, embeddings, and document APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upstage-deployment](https://clawhub.ai/user/upstage-deployment)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Upstage-powered applications, RAG systems, document processing pipelines, and Agent API workflows. It helps choose Solar models and generate code, configuration, shell commands, and deployment guidance for Upstage API projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples and generated workflows may send prompts, documents, and API requests to Upstage services.

Mitigation: Use the skill only for data intended for Upstage processing, configure UPSTAGE_API_KEY through the environment, and avoid hardcoding credentials.

Risk: Helper scripts can create or overwrite scaffold files and refresh mutable reference documentation.

Mitigation: Review the target project slug and changed files before running helper scripts or deploying generated webapps.

Risk: Production applications could expose model reasoning or sensitive document-derived output to end users.

Mitigation: Pin dependencies, review generated interfaces, and keep internal reasoning or sensitive extracted data out of public views.

## Reference(s):

- [Upstage Builder Skill](https://clawhub.ai/upstage-deployment/skills/upstage-builder)
- [Upstage API Docs](https://console.upstage.ai/api/docs/for-agents/raw)
- [Upstage Console](https://console.upstage.ai)
- [Upstage Studio](https://studio.upstage.ai)
- [Chat Completions API](references/chat-completions.md)
- [Embeddings API](references/embeddings.md)
- [Document Processing](references/document-processing.md)
- [Information Extraction](references/information-extraction.md)
- [Document Classification](references/document-classification.md)
- [Agent API](references/agent-api.md)
- [Common Patterns](references/common-patterns.md)
- [Webapp Workflow](references/webapp-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, command snippets, configuration notes, and generated project files when scaffolding is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API calls and local files for Upstage examples, RAG pipelines, document workflows, or webapp scaffolds.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
