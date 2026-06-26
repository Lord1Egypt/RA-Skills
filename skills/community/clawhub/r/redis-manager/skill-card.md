## Description: <br>
Manage a shared Redis Docker container for local dev environments. Handles container lifecycle, key inspection, and selective data flush. Joins the shared Docker network created by proxy-manager. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pereirajair](https://clawhub.ai/user/pereirajair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to start, stop, inspect, and clean up a shared local Redis Docker container during application development and testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Redis data can be deleted when flush commands are explicitly run. <br>
Mitigation: Review the target container and database before confirming any flush, and prefer flush-db for scoped cleanup. <br>
Risk: The default Redis password may be unsuitable on shared machines or with non-disposable data. <br>
Mitigation: Set REDIS_PASSWORD before use in shared environments or when working with data that should be protected. <br>
Risk: The Redis container uses a restart policy and may continue running after Docker restarts. <br>
Mitigation: Run the stop command when the shared local Redis service is no longer needed. <br>


## Reference(s): <br>
- [Redis Manager ClawHub page](https://clawhub.ai/pereirajair/redis-manager) <br>
- [pereirajair publisher profile](https://clawhub.ai/user/pereirajair) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker on Linux or macOS and operates on a local Redis container] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
