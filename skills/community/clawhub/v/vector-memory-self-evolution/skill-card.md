## Description: <br>
This skill helps an agent capture user-derived errors, corrections, best practices, and events into a local BGE and Chroma-backed vector memory system for later semantic retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxbl79](https://clawhub.ai/user/lxbl79) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent local memory capture, semantic search, conflict checks, and pre-execution reminders to an OpenClaw-style workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses user-derived data persistently in local files and vector databases. <br>
Mitigation: Treat memory files and vectors as sensitive data, avoid storing secrets, and review retention and backup behavior before enabling broad capture. <br>
Risk: Auto-capture, cron jobs, and rule promotion can preserve or reuse incorrect or sensitive guidance without enough review. <br>
Mitigation: Keep autoCapture and scheduled jobs disabled until reviewed, and require manual approval before writing durable rules to SOUL.md or reusing memory as future agent guidance. <br>
Risk: Vectorization depends on a localhost service on port 11434. <br>
Mitigation: Verify which service owns localhost:11434 before sending memory content for embeddings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxbl79/vector-memory-self-evolution) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lxbl79) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation, Python APIs, shell commands, local markdown memory files, and Chroma vector search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files under ~/.openclaw/workspace and a localhost embedding service on port 11434 when vectorizing memories.] <br>

## Skill Version(s): <br>
2.1.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
