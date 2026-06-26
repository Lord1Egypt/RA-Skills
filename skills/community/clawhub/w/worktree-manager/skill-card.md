## Description: <br>
Manage Docker-based dev instances and git worktrees, including app container lifecycle, database seeding, and proxy route activation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pereirajair](https://clawhub.ai/user/pereirajair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage local Docker-based development instances and isolated git worktrees for application changes. It helps start, stop, inspect, create, and remove per-worktree environments that depend on shared MySQL and proxy services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has powerful environment administration behavior and can affect services when commands are run against sensitive targets. <br>
Mitigation: Review the intended inventory, target environment, and command scope before execution; avoid production targets unless the operator explicitly intends that impact. <br>
Risk: Removing a worktree is destructive and can delete containers, an instance database, a git worktree, its branch, and its environment file. <br>
Mitigation: Require explicit confirmation before removal, run the list command first, and verify backups or recovery options for any valuable database state. <br>
Risk: Using the default MySQL root password can expose local development data or make accidental cross-environment access easier. <br>
Mitigation: Set MYSQL_ROOT_PASSWORD for environments that matter and verify the target MySQL container before starting or seeding instances. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pereirajair/worktree-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires docker and git on Linux or Darwin; expects mysql-manager and proxy-manager services to be started first.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
