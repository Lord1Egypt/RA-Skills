## Description: <br>
Siyuan Skill gives an agent a Node.js CLI for managing SiYuan Notes notebooks, documents, content search, and block-level operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dazexcl](https://clawhub.ai/user/dazexcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent operate a configured SiYuan Notes workspace through CLI commands. It supports notebook and document management, content retrieval and editing, block operations, search, optional vector indexing, and NLP analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change a broad range of SiYuan Notes content, including document and block operations. <br>
Mitigation: Review the requested operation before execution, use a least-privilege SiYuan token, and prefer whitelist permission mode. <br>
Risk: Vector indexing and search can process notebook content that may include sensitive notes. <br>
Mitigation: Avoid indexing sensitive notebooks and keep Qdrant and embedding services on trusted local infrastructure. <br>
Risk: Some documented SQL-injection and permanent-protection guarantees are not considered reliable by the security evidence. <br>
Mitigation: Do not rely on those guarantees until fixed; treat deletion, SQL-related, and protection-sensitive operations as requiring explicit user review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dazexcl/siyuan-skill) <br>
- [Installation and setup](references/config/setup.md) <br>
- [Environment configuration](references/config/environment.md) <br>
- [Advanced configuration and security](references/config/advanced.md) <br>
- [Command reference](references/commands/) <br>
- [Vector search guide](references/advanced/vector-search.md) <br>
- [Best practices](references/advanced/best-practices.md) <br>
- [SiYuan Notes API](https://github.com/siyuan-note/siyuan/blob/master/API_zh_CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text guidance with inline shell commands and JSON-style CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate against a configured SiYuan Notes instance and may read, create, update, move, delete, search, or index notebook content depending on user intent and configuration.] <br>

## Skill Version(s): <br>
1.7.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
