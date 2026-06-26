## Description: <br>
XiaoShan Memory Engine provides persistent AI memory with semantic search, knowledge graph queries, memory statistics, and delete/forget operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waychan8](https://clawhub.ai/user/waychan8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to save, search, recall, ask questions over, list, and delete local AI memories through a localhost memory service. It is useful for agents that need persistent memory, semantic retrieval, and knowledge graph summaries across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release uses a remote install/update source that should be reviewed before use. <br>
Mitigation: Verify the remote source and artifact contents before installation, and prefer a pinned, reviewed release in managed environments. <br>
Risk: The skill stores persistent local memory and may send memory-related content to configured AI providers. <br>
Mitigation: Avoid storing secrets or regulated data, protect local configuration and data files, and prefer local-provider mode for sensitive use. <br>
Risk: Save and forget/delete actions can persist or remove user memory state. <br>
Mitigation: Require explicit user confirmation for save and forget/delete operations, and keep exports or backups when memory retention matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/waychan8/xiaoshan-memory) <br>
- [XiaoShan Memory HTTP API Reference](references/api.md) <br>
- [XiaoShan Memory homepage](http://152.136.24.34) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and HTTP API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local state under ~/.xiaoshan and provider API credentials when configured.] <br>

## Skill Version(s): <br>
3.3.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
