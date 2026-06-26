## Description: <br>
Persistent local transcript-first memory for OpenClaw via a Node adapter and FastAPI engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluepointdigital](https://clawhub.ai/user/bluepointdigital) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Smart Memory to give OpenClaw-style local agents durable, transcript-backed recall of prior decisions, preferences, goals, and task state through a localhost FastAPI backend. It supports memory search, memory commits, transcript inspection, prompt composition, and pending insight retrieval for local agent continuity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores conversation history and can later surface that history during agent sessions. <br>
Mitigation: Use it only when durable local memory is intended, avoid putting secrets in persisted chats, and review the SQLite and hot-memory file locations before deployment. <br>
Risk: The local backend should not be exposed beyond the host machine. <br>
Mitigation: Keep the FastAPI server bound to 127.0.0.1 and verify host and port settings before starting the service. <br>
Risk: Setup downloads Python and Node dependencies, and the default embedding model enables trusted remote model code execution unless changed. <br>
Mitigation: Review installation behavior and dependency sources before running setup, and change the embedding configuration if trusted remote model code is not acceptable. <br>


## Reference(s): <br>
- [Smart Memory README](README.md) <br>
- [Smart Memory Skill Definition](SKILL.md) <br>
- [OpenClaw Skill README](skills/smart-memory-openclaw/README.md) <br>
- [Integration Guide](INTEGRATION.md) <br>
- [Memory Structure](MEMORY_STRUCTURE.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured tool responses with code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include retrieved memory context, persisted memory acknowledgements, pending insight summaries, transcript inspection results, and bounded prompt context.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata; artifact changelog and package.json report 3.1.0-experimental) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
