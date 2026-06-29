## Description: <br>
Xby Todolist provides external working memory and structured task management for large language models and AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent read and update a session todo list through the XiaoBenYang task-memory API during complex, multi-step work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo content is sent to the XiaoBenYang API as a third-party task-memory provider. <br>
Mitigation: Use the skill only for task data appropriate for that provider and avoid passwords, tokens, private customer data, or other sensitive material in todos. <br>
Risk: The API key is saved locally in a .env file as XBY_APIKEY rather than in an operating-system secrets manager. <br>
Mitigation: Protect the local workspace, avoid committing .env files, and rotate the API key if it may have been exposed. <br>


## Reference(s): <br>
- [Xby Todolist on ClawHub](https://clawhub.ai/alinklab/xby-todolist) <br>
- [XiaoBenYang](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP API](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration] <br>
**Output Format:** [Markdown summaries of JSON responses from todo read and write operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided XBY API key and sends todo content to the XiaoBenYang API.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
