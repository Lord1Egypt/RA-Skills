## Description: <br>
Provides a layered persistent memory system for AI assistants, with tagged retrieval, reliability ratings, periodic organization, and configurable IMA knowledge-base synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taobaoaz](https://clawhub.ai/user/taobaoaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-assistant users use this skill to store, retrieve, organize, and synchronize cross-session memories, decisions, project knowledge, and lessons learned. It is most relevant when an assistant needs durable context across conversations or workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist broad personal, project, or workspace memory across sessions. <br>
Mitigation: Use it only when long-term memory is intended, review memory files regularly, and avoid storing secrets, credentials, private identifiers, health, financial, or confidential business data. <br>
Risk: IMA synchronization can upload memory content to external notes when enabled and configured. <br>
Mitigation: Disable IMA sync unless needed, replace default note mappings with destinations under the user's control, and use a limited IMA key. <br>
Risk: Weak consent or scope controls may cause more information to be retained or synced than expected. <br>
Mitigation: Require explicit user confirmation before writing or syncing sensitive memory, and review queued content before upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taobaoaz/yaoyaoya-memory) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Example configuration](artifact/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown memory files, JSON configuration, Python helper commands, and concise assistant guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local memory files and, when configured, synchronize selected content to IMA notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
