## Description: <br>
语雀 (Yuque) 知识库管理。搜索、阅读、创建、编辑语雀文档，管理知识库和目录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lt5227](https://clawhub.ai/user/lt5227) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent search, read, create, edit, delete, and organize Yuque knowledge base content through Yuque OpenAPI scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store a Yuque API token in a local config.json file. <br>
Mitigation: Use a limited-scope Yuque token when possible and prefer an environment variable or protected secret storage over plaintext local configuration. <br>
Risk: The skill can delete remote Yuque documents. <br>
Mitigation: Require the agent to show the exact repository and document target and get explicit confirmation before any delete operation. <br>
Risk: Document content may be written locally and sent to Yuque. <br>
Mitigation: Avoid using the skill for highly sensitive documents unless local handling and Yuque upload are acceptable. <br>


## Reference(s): <br>
- [Yuque OpenAPI v2 Reference](references/api-reference.md) <br>
- [Yuque](https://www.yuque.com) <br>
- [ClawHub skill page](https://clawhub.ai/lt5227/yuque-knowledge-base) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts write JSON to stdout and send errors to stderr.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
