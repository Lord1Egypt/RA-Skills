## Description: <br>
Delegates coding tasks to Codex, Claude Code, Pi, or OpenCode agents through foreground or background shell sessions with guidance for PTY use, workdirs, monitoring, and cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TSHOGX](https://clawhub.ai/user/TSHOGX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to delegate implementation, refactoring, PR review, and multi-worktree coding tasks to local coding-agent CLIs while monitoring and controlling sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes unsandboxed or approval-bypassing agent runs that may read or modify repositories and use local CLI credentials. <br>
Mitigation: Install only when intentional, prefer sandboxed modes, avoid --yolo and bypassPermissions unless the repository and provider are trusted, and run work in temp clones or git worktrees. <br>
Risk: Delegated agents can produce external side effects such as GitHub comments, pushes, or pull requests. <br>
Mitigation: Manually review diffs, comments, pushes, and pull requests before publishing or merging agent output. <br>
Risk: Long-running background jobs can continue modifying a workspace after launch. <br>
Mitigation: Set timeouts, monitor session logs, and terminate sessions that no longer match the requested task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TSHOGX/tshogx-coding-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands for foreground or background execution, session monitoring, input, cleanup, and PR workflow steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
