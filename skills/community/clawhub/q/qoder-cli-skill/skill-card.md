## Description: <br>
Delegates coding, code review, refactoring, and iterative file-exploration tasks to Qoder CLI using non-interactive Print mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lfeng](https://clawhub.ai/user/lfeng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to delegate larger coding tasks to Qoder CLI when work benefits from automated file exploration, implementation, refactoring, code review, subagents, worktrees, or MCP integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes permission-bypassing through Qoder CLI yolo mode. <br>
Mitigation: Avoid yolo mode except in isolated, non-sensitive workspaces and prefer explicit Qoder CLI permission controls. <br>
Risk: The skill relies on an authenticated third-party coding CLI that can operate on the user's codebase. <br>
Mitigation: Install only when the qodercli binary and Qoder account context are trusted, and review proposed file or command changes before use. <br>
Risk: MCP servers can extend Qoder CLI with additional external tools. <br>
Mitigation: Review each MCP server before adding it and limit use to trusted servers required for the task. <br>
Risk: Shared sessions may allow other participants to influence prompts run under the user's token. <br>
Mitigation: Use caution in shared sessions and avoid running sensitive authenticated tasks from prompts supplied by untrusted participants. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lfeng/qoder-cli-skill) <br>
- [Publisher profile](https://clawhub.ai/user/lfeng) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the qodercli binary and uses Qoder CLI Print mode for non-interactive execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
