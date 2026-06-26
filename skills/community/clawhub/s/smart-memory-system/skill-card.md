## Description: <br>
Provides retrieval-augmented semantic memory search, indexing, and context enhancement for OpenClaw conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jazzqi](https://clawhub.ai/user/jazzqi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to index local memories or knowledge sources, retrieve relevant history by semantic similarity, and inject selected context into conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists and automatically reuses user history, which can expose sensitive or irrelevant stored content in later prompts. <br>
Mitigation: Use narrow memory sources, review what is indexed, and confirm backup and deletion behavior before relying on automatic context enhancement. <br>
Risk: Memory content may be sent to configured embedding or reranking providers during retrieval workflows. <br>
Mitigation: Confirm provider data-handling terms and avoid indexing private folders or sensitive documents until the data flow is understood. <br>
Risk: Automatic context enhancement can add stale or low-quality memories to a conversation. <br>
Mitigation: Prefer disabling auto-enhance initially, monitor retrieved context, and tune similarity thresholds before broad use. <br>


## Reference(s): <br>
- [Smart Memory System ClawHub Page](https://clawhub.ai/jazzqi/smart-memory-system) <br>
- [README](artifact/README.md) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Package Metadata](artifact/package.json) <br>
- [Smart Memory Configuration](artifact/config/smart_memory.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JavaScript snippets, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory indexes, semantic caches, backups, logs, and configuration files under the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
