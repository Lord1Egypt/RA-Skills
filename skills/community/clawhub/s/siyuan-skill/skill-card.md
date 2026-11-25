## Description:

Provides a Node.js CLI for agents to manage SiYuan notebooks, documents, content search, tags, and block-level operations through the SiYuan API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dazexcl](https://clawhub.ai/user/dazexcl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent inspect and modify a local SiYuan knowledge base, including notebook listing, document creation and updates, search, tagging, and block operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional vector indexing can expose note content to configured Qdrant or embedding services.

Mitigation: Use local trusted Qdrant and Ollama services where possible, and only configure remote services when their operators and data handling are trusted.

Risk: Forced or removal indexing operations can erase or bypass scoped indexes without enough safeguards.

Mitigation: Avoid running index --force or index --remove unless the target document or notebook scope is explicit and reviewed.

Risk: A SiYuan token gives the agent access to the configured notes workspace.

Mitigation: Use only a token intended for agent use and prefer whitelist mode for notebook access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dazexcl/skills/siyuan-skill)
- [Setup Guide](references/config/setup.md)
- [Environment Configuration](references/config/environment.md)
- [Vector Search Configuration](references/advanced/vector-search.md)
- [SiYuan API](https://github.com/siyuan-note/siyuan/blob/master/API_zh_CN.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON-like command responses, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include SiYuan document content, search results, block identifiers, notebook metadata, and configuration guidance.]

## Skill Version(s):

1.7.8 (source: server release evidence and artifact index.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
