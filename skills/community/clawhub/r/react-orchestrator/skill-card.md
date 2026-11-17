## Description:

React Orchestrator is a Node.js ReAct and Reflexion orchestration library that routes tasks between a fast System 1 path and a deeper reflective System 2 path while coordinating registered tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to build agents that select fast or reflective reasoning paths, register external tools, and return auditable task execution results. It is suited to multi-step search, retrieval, file, code, and planning workflows where task complexity determines the execution mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute generated JavaScript and PowerShell code and includes file read/write templates, creating host-level code and file access risk.

Mitigation: Disable or isolate Code Mode before using real data; if enabled, run it in a least-privileged sandbox with an approved workspace and no inherited secrets.

Risk: PowerShell execution uses an execution-policy bypass path.

Mitigation: Remove or disable PowerShell execution unless explicitly required, and require review before any PowerShell-backed tool is registered or invoked.

Risk: Human approval is implemented as a helper and may not be enforced before every sensitive tool call.

Mitigation: Enforce HITL centrally around all file-write, command-execution, deletion, network, and other sensitive tools with timeout rejection and a narrow auto-approve list.

Risk: Reasoning mode selection, semantic tool matching, and parameter extraction rely on heuristics or simplified implementations in this version.

Mitigation: Validate tool parameters with schemas, review high-impact actions, keep execution timeouts enabled, and inspect execution history before relying on results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/react-orchestrator)
- [README](artifact/README.md)
- [Usage Guide](artifact/USAGE-GUIDE.md)
- [Quick Reference](artifact/QUICK-REFERENCE.md)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Reflexion Paper](https://arxiv.org/abs/2303.11366)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JavaScript snippets, shell commands, configuration examples, and JSON-like execution result objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary results include an answer, execution history, selected mode, iteration count, duration, and optional reflections or command output.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
