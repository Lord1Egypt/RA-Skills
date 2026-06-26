## Description: <br>
Strategic Compact guides agents to compact conversation context at logical workflow boundaries and optionally monitor long sessions with a local tool-call counter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill during long or multi-phase sessions to decide when to compact context, preserve important state in files, and continue work from a cleaner conversation history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compacting before saving important context can lose conversation history, tool output, and unsaved reasoning. <br>
Mitigation: Save key findings to files, update task notes, and preserve git state before invoking /compact. <br>
Risk: Optional hook or cron integration can create recurring local checks and /tmp counter files. <br>
Mitigation: Enable recurring integrations only intentionally, and remove /tmp/claude-tool-count-* files between unrelated sessions when needed. <br>


## Reference(s): <br>
- [Strategic Compaction Guide](references/compaction-guide.md) <br>
- [Tool Integration Guide](references/tool-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional script invocation writes a session counter under /tmp.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
