## Description: <br>
Persistent memory toolkit for AI agents that saves context, recalls memories with relevance scoring, consolidates insights, and tracks decisions across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swaylq](https://clawhub.ai/user/swaylq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to persist useful session context, search or load prior memories, review topic history, and manage backups for local agent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memories and backups are stored as local plaintext files and may contain sensitive session details. <br>
Mitigation: Do not store API keys, passwords, tokens, or raw sensitive details; use vault references and protect memory directories, exports, and backups as sensitive files. <br>
Risk: Script input-handling bugs may allow crafted arguments or imported content to affect shell or Node execution. <br>
Mitigation: Review script arguments before execution, avoid untrusted prompt-controlled arguments and imported backups, and deploy only after the input-interpolation issues are fixed or accepted. <br>
Risk: Replayed memories can inject stale, incorrect, or untrusted context into later agent sessions. <br>
Mitigation: Review recalled context before relying on it for decisions, delete or edit obsolete entries, and keep critical memories concise and source-aware. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/swaylq/session-memory) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown-style CLI text, JSON arrays or objects, JSONL memory files, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores memories as local plaintext JSONL under AGENT_MEMORY_DIR or ~/.agent-memory; requires node.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
