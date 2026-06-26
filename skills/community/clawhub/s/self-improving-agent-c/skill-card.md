## Description: <br>
Captures learnings, errors, corrections, and feature requests so agents can preserve useful lessons for future work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenhaoyu521](https://clawhub.ai/user/chenhaoyu521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to record command failures, user corrections, feature requests, and recurring work patterns in local markdown files. The records can then be reviewed or promoted into project memory, workspace guidance, or new reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local learning logs may accidentally capture secrets, private command output, or full transcripts. <br>
Mitigation: Record short sanitized summaries by default, redact sensitive values, and only include full details when the user explicitly requests it. <br>
Risk: Opt-in hooks run in the project environment and the error detector reads command output for error patterns. <br>
Mitigation: Keep hooks project-scoped where possible, review hook scripts before enabling them, and enable PostToolUse error detection only in trusted workspaces. <br>
Risk: Incorrect or low-value lessons could be promoted into durable agent guidance. <br>
Mitigation: Review entries before promotion and keep promoted guidance concise, sourceable, and scoped to the relevant project or workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenhaoyu521/self-improving-agent-c) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, templates, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends local .learnings markdown files when the agent follows the workflow; optional hooks emit reminder text.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
