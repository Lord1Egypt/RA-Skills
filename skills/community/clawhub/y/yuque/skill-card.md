## Description: <br>
Manage Yuque knowledge base documents and repositories for reading documents, listing repositories, searching content, creating documents, and managing knowledge bases in personal and team spaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a6590072](https://clawhub.ai/user/a6590072) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base operators use this skill to let an agent work with Yuque repositories and documents through authenticated API calls, including reading, listing, searching, creating, and updating content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Yuque API token to read and change documents. <br>
Mitigation: Use the narrowest available token and only install the skill when agent access to Yuque is intended. <br>
Risk: Create or update operations can modify knowledge-base content. <br>
Mitigation: Review proposed create and update requests before execution. <br>
Risk: The bundled client contains a document deletion method even though the CLI does not expose it. <br>
Mitigation: Review any agent-generated code or direct helper use before allowing delete-capable operations. <br>


## Reference(s): <br>
- [Yuque API Reference](references/api.md) <br>
- [Yuque API Base URL](https://www.yuque.com/api/v2) <br>
- [ClawHub Skill Page](https://clawhub.ai/a6590072/yuque) <br>
- [Publisher Profile](https://clawhub.ai/user/a6590072) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python helper usage, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Yuque API token for authenticated operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
