## Description: <br>
Swarm Sprint helps agents coordinate parallel coding sprints by planning task conflicts, creating isolated git worktrees and branches, and preparing subagent work packages for review and merge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdh3](https://clawhub.ai/user/jdh3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering coordinators use this skill when they have two or more coding tasks in one repository and want an agent to plan conflicts, create isolated worktrees, assign subagents, and review changes before merging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup and command execution can delete local worktrees or branches too broadly if used on an important repository without review. <br>
Mitigation: Use the skill only on disposable or backed-up repositories, inspect swarm-packages.json before cleanup, and confirm branch and worktree paths before deletion. <br>
Risk: Untrusted task IDs or task files can influence generated commands, branch names, and worktree paths. <br>
Mitigation: Use trusted task files with simple task IDs, run the plan-only mode first, and review generated worktree paths before creating or cleaning up worktrees. <br>
Risk: Parallel agent changes can still introduce incorrect code or integration issues even when file conflicts are planned. <br>
Mitigation: Review every diff, merge one branch at a time, and run the repository's type checks and tests after each merge. <br>


## Reference(s): <br>
- [Swarm Sprint on ClawHub](https://clawhub.ai/jdh3/swarm-sprint) <br>
- [Example Tasks](references/example-tasks.json) <br>
- [Test Tasks](references/test-tasks.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown instructions with bash command examples and JSON task/package files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates per-task worktree instructions and a swarm-packages.json file when run; supports plan-only and dry-run modes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
