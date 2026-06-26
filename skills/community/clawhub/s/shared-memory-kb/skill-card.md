## Description: <br>
为 OpenClaw 用户所有 Agent 身份提供统一的跨身份共享记忆层，支持写入、检索、浏览、关联和回顾个人知识库；当用户需要记录洞察、检索经验、总结知识或定期回顾时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ludiansheng](https://clawhub.ai/user/ludiansheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and their agents use this skill to maintain a shared local personal knowledge base across agent identities. It helps agents store, retrieve, browse, link, and summarize reusable insights, experiences, decisions, and knowledge records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad, automatic, cross-persona persistence and retrieval of personal conversation content. <br>
Mitigation: Use manual confirmation for writes when appropriate, keep the storage path private, and review or prune memory files regularly. <br>
Risk: Long-lived memory records can expose sensitive information in later contexts. <br>
Mitigation: Avoid saving secrets, credentials, health or financial details, and private third-party information unless the user has explicitly accepted later reuse. <br>
Risk: Cross-identity retrieval can mix personal, work, learning, and other persona-specific records. <br>
Mitigation: Apply persona filters and category tags when querying, linking, or generating reflections. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ludiansheng/shared-memory-kb) <br>
- [Configuration reference](references/CONFIG.md) <br>
- [Data model reference](references/DATA_MODEL.md) <br>
- [Taxonomy reference](references/TAXONOMY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent to operate a local memory store and present retrieved or summarized memory content in natural language.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
