## Description: <br>
Helps agents isolate troubleshooting work in a temporary Git worktree or subagent so the main conversation context can continue after the issue is resolved. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[graceqx](https://clawhub.ai/user/graceqx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill when an error or defect needs focused investigation without polluting the main task context. It guides creation of an isolated worktree or subagent session, records troubleshooting state, and helps apply or discard the isolated changes after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper scripts can create temporary Git branches and worktree directories, merge troubleshooting changes, and force-remove the isolated worktree and branch. <br>
Mitigation: Commit or back up important work before use, invoke commands explicitly, and review proposed changes before applying or discarding the isolated session. <br>
Risk: Broad activation wording can start a troubleshooting flow when the user only meant to describe a problem. <br>
Mitigation: Confirm user intent before running helper scripts or changing repository state, and prefer explicit command invocation for repository operations. <br>
Risk: Troubleshooting records may include project paths, branch names, issue titles, or solution notes. <br>
Mitigation: Review .trouble-shooting records before sharing a repository or publishing logs, especially when issue titles or paths may be sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/graceqx/trouble-shooting) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with JSON status output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts may emit issue IDs, session status, archive paths, and cleanup results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
