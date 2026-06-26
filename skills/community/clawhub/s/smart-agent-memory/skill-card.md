## Description: <br>
Smart Agent Memory provides a local long-term memory CLI for OpenClaw agents, with layered context retrieval, fact, lesson, entity, and session storage, search, reflection, archiving, and optional SQLite/FTS5 storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beyound87](https://clawhub.ai/user/beyound87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give OpenClaw agents a durable local memory across sessions. It supports recording and retrieving facts, lessons, entities, skill experience, and session summaries while encouraging scoped retrieval instead of loading all memory at once. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can modify every ~/.openclaw/workspace* workspace by appending BOOTSTRAP.md memory-start instructions. <br>
Mitigation: Review the BOOTSTRAP text before running setup, run setup only where workspace-wide memory behavior is intended, and inspect workspace changes afterward. <br>
Risk: Durable local memory can retain secrets, regulated data, or private personal details if users record them. <br>
Mitigation: Do not store credentials, regulated data, or private personal details; periodically review and delete memory entries that should not persist. <br>
Risk: The extract command can generate new skills from lessons that may carry over incorrect or unsafe guidance. <br>
Mitigation: Manually review and scan generated skills before enabling or publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beyound87/smart-agent-memory) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/beyound87) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text and JSON output, Markdown memory files, generated SKILL.md files, and BOOTSTRAP.md configuration text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OpenClaw memory files by default; setup appends BOOTSTRAP.md instructions to discovered workspaces; SQLite/FTS5 storage requires a Node.js runtime with node:sqlite support.] <br>

## Skill Version(s): <br>
3.0.6 (source: server release evidence; artifact frontmatter reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
