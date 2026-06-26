## Description: <br>
Coordinates multiple Codex agents in isolated git worktrees so developers can split coding work into parallel tasks, monitor progress, and combine the results through commits and pull requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[InuyashaYang](https://clawhub.ai/user/InuyashaYang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to decompose a repository task into file-scoped work items, launch parallel coding agents in separate worktrees, monitor logs, and prepare resulting branches or pull requests for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give autonomous coding agents broad authority to write, commit, push, open pull requests, and potentially merge code. <br>
Mitigation: Use it only with repositories where that authority is acceptable, review diffs manually before push or merge, and prefer dedicated low-scope GitHub tokens. <br>
Risk: Logs, local file paths, or code excerpts may be exposed through the dashboard or optional model-based analysis. <br>
Mitigation: Bind the dashboard to localhost or add authentication, avoid sensitive repositories, and disable third-party analysis unless log sharing is intentional. <br>
Risk: Parallel worktrees can create conflicting or incorrect changes if task ownership is vague. <br>
Mitigation: Assign each file to a single agent, keep dependent tasks serial, and require final human review before integrating branches. <br>


## Reference(s): <br>
- [Worktree Agents Task Decomposition Reference](references/task-decomposition.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/InuyashaYang/worktree-codex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, task prompts, log-monitoring instructions, and pull request workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce worktree setup output, agent log paths, commits, branches, and pull request URLs when the user runs the provided scripts.] <br>

## Skill Version(s): <br>
1.1.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
