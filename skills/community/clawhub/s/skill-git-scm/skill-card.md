## Description: <br>
Clones a Git repository to a local path or updates an existing checkout from a selected branch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lentiancn](https://clawhub.ai/user/lentiancn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to clone a remote Git repository or update an existing local checkout by branch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can clone or update repositories in a caller-specified local path, which may change files on disk. <br>
Mitigation: Confirm GIT_REMOTE_URL, GIT_LOCAL_PATH, and GIT_BRANCH before execution and run it only in intended workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lentiancn/skill-git-scm) <br>
- [Publisher skills repository](https://github.com/lentiancn/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [Plain text status messages and shell command invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script reports SUCCESS for clone or update operations and ERROR for missing inputs or directory access failures.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
