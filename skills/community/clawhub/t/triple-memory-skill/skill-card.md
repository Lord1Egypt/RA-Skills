## Description: <br>
Complete memory system combining LanceDB auto-recall, Git-Notes structured memory, and file-based workspace search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ktpriyatham](https://clawhub.ai/user/ktpriyatham) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure persistent agent memory across conversation recall, structured decision logging, and workspace-file search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic persistent memory can silently store and reuse user or workspace context with limited user visibility. <br>
Mitigation: Enable the skill only when persistent memory is intended, remove or override silent-operation instructions, and ensure stored memories can be inspected, edited, and deleted. <br>
Risk: Auto-capture and pre-compaction flushing can preserve sensitive conversation or workspace details. <br>
Mitigation: Disable auto-capture and auto-flush for sensitive work and define excluded paths and data categories before deployment. <br>
Risk: Embedding-backed memory may send text to the configured embedding provider. <br>
Mitigation: Confirm what text is sent for embeddings and configure provider access and retention controls before using the skill. <br>


## Reference(s): <br>
- [Triple Memory Setup Reference](references/SETUP.md) <br>
- [Auto Flush Configuration](references/auto-flush-config.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/ktpriyatham/triple-memory-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the memory-lancedb plugin, the git-notes-memory skill, an embedding API key for LanceDB memory, and workspace file access.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
