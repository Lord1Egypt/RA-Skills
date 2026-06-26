## Description: <br>
Operate RAGFlow v0.26.0 deployments through a bundled Node CLI and API client for datasets, documents, retrieval, chat assistants, agents, model providers, system settings, and diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunarcache](https://clawhub.ai/user/lunarcache) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage RAGFlow deployments, including knowledge bases, document ingestion and parsing, retrieval workflows, chat and agent sessions, embedded access, model/provider configuration, and diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run administrative commands against a RAGFlow deployment using RAGFLOW_API_KEY. <br>
Mitigation: Install it only for intended RAGFlow administration, use a scoped API key, and prefer HTTPS for production deployments. <br>
Risk: Delete commands can irreversibly remove datasets, documents, chunks, chats, sessions, agents, connectors, providers, or tokens. <br>
Mitigation: Confirm destructive operations before execution unless cleaning temporary resources created in the same workflow. <br>
Risk: Embed tokens, connector credentials, provider API keys, and generated auth URLs can expose operational access. <br>
Mitigation: Treat these values as secrets and redact token, beta, auth URL, and API key material unless the user explicitly requests it. <br>


## Reference(s): <br>
- [RAGFlow Skill repository](https://github.com/LunarCache/ragflow-skill) <br>
- [RAGFlow Custom Agent Guide](references/AGENT_GUIDE.md) <br>
- [Programmatic API and Configuration](references/API.md) <br>
- [Command Reference](references/COMMANDS.md) <br>
- [Output Format Reference](references/REFERENCE.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, tables, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers raw JSON for command chaining and concise summarized Markdown for user-facing responses.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
