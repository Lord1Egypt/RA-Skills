## Description: <br>
Autonomously handles debugging and coding recovery workflows when an agent encounters code errors, build failures, stack traces, or unexpected behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grimmjoww](https://clawhub.ai/user/grimmjoww) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to guide coding agents through debugging, test reruns, minimal code edits, git checks, and escalation to dedicated coding agents when a task becomes complex. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage broad automatic repair behavior, including file edits, command execution, and background delegation. <br>
Mitigation: Use it in a branch or disposable workspace and require confirmation before file edits, package installs, destructive commands, or background delegation. <br>
Risk: Spawned coding agents may make changes outside the main agent's immediate context. <br>
Mitigation: Review diffs and spawned-agent logs before accepting changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/grimmjoww/ultra-agent-stinct) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Git Workflow Reference](references/git-workflow.md) <br>
- [Escalation Guide](references/escalation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
