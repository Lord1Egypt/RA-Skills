## Description: <br>
Provides a layered long-term memory system for storing, searching, organizing, and reusing agent memories with hybrid search, atomic transactions, WAL support, and plugin-based extensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mouxangithub](https://clawhub.ai/user/mouxangithub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give agents persistent memory: storing conversation-derived facts, searching prior context, exporting or deleting memories, and maintaining memory indexes across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically record, index, and reuse conversation-derived memory in future prompts. <br>
Mitigation: Install only when persistent memory is intended, review what is captured, and confirm users can inspect, delete, export, and disable stored memories. <br>
Risk: The submitted install package is incomplete and its access scope is broader than disclosed. <br>
Mitigation: Verify the real install source before deployment and keep cloud, provider, wallet, or other sensitive credentials disabled unless they are explicitly required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mouxangithub/unified-memory-v5) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/mouxangithub) <br>
- [README](artifact/README.md) <br>
- [Installation Guide](artifact/INSTALL.md) <br>
- [Technical Reference](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Agent responses, MCP tool results, memory records, exported memory data, and operational commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store and retrieve conversation-derived memory, indexes, evidence chains, transcript records, and exported memory files.] <br>

## Skill Version(s): <br>
5.2.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
