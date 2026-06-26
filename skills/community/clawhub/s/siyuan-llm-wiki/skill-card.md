## Description: <br>
Helps an AI agent build and maintain a structured LLM Wiki knowledge base in SiYuan Notes using the SiYuan HTTP API, source summaries, entity pages, concept pages, synthesis pages, and backlinks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whiteless9](https://clawhub.ai/user/whiteless9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to have an agent organize articles, notes, and conversations into a SiYuan-hosted personal knowledge base. It supports ingestion, querying, synthesis, indexing, and maintenance workflows for structured knowledge management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad write access to a SiYuan notebook and may create, update, or archive notes. <br>
Mitigation: Use a dedicated SiYuan notebook, keep a backup or snapshot, and require preview and confirmation before every create, update, or archive action. <br>
Risk: SiYuan API tokens and notebook identifiers are needed for operation and could be exposed if pasted into chat or saved in logs. <br>
Mitigation: Provide tokens through environment variables or a secret store, avoid sharing credentials in conversation text, and rotate the token if exposure is suspected. <br>
Risk: Conversation or source content may be saved into the knowledge base without clear per-write consent. <br>
Mitigation: Avoid auto-archiving private, confidential, or credential-like conversations, and ask the user to approve any content before it is persisted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whiteless9/siyuan-llm-wiki) <br>
- [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>
- [SiYuan API documentation](https://leolee9086.github.io/siyuan-kernelApi-docs/) <br>
- [SiYuan community API summary](https://www.siyuan-note.club/llms.txt) <br>
- [SiYuan GitHub API documentation](https://github.com/siyuan-note/siyuan/blob/master/API_zh_CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash examples, Python helper code, and reusable page templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SiYuan document content, API request examples, SQL query examples, and maintenance guidance for agent-operated knowledge bases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
