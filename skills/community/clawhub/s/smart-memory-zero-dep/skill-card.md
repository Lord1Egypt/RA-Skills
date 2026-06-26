## Description: <br>
Enhanced memory system for agentic workflows with automatic memory extraction, memory type classification, temporal decay and archival, session-scoped temporary cache, and HOT RAM working memory with a WAL protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zgjq](https://clawhub.ai/user/zgjq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to persist useful conversation-derived memory, manage current task state, classify and promote durable notes, and maintain local memory hygiene across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores conversation-derived preferences, project facts, lessons, and task state on local disk. <br>
Mitigation: Use it only for conversations suitable for durable local memory, require confirmation before durable writes or cleanup, and avoid running it on sensitive conversations or credentials. <br>
Risk: A restore feature can load arbitrary local files into active agent memory. <br>
Mitigation: Restrict restore operations to the session-snapshots directory and confirm the target file before loading it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zgjq/smart-memory-zero-dep) <br>
- [Memory Schema Reference](references/memory_schema.md) <br>
- [Memory Extraction Prompt Template](references/extraction_prompt.md) <br>
- [Decay & Archival Rules](references/decay_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory files, session state, cache entries, health reports, classification suggestions, and archival actions when invoked through its scripts.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
