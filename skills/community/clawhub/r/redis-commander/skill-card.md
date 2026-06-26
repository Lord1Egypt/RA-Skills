## Description: <br>
Manage the Redis Commander Docker container for local development environments, providing a local web UI for Redis key inspection at http://localhost:8083. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pereirajair](https://clawhub.ai/user/pereirajair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to start, stop, inspect, and access a local Redis Commander web UI for Redis data inspection in development environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default Redis Commander and Redis passwords may expose sensitive Redis data on shared machines. <br>
Mitigation: Change the default Commander and Redis passwords before use on shared machines or with sensitive data. <br>
Risk: The Redis Commander container uses a restart policy and can continue running after reboot. <br>
Mitigation: Stop the container when finished and verify its status with the provided lifecycle command. <br>
Risk: The skill is intended for local development Redis environments only. <br>
Mitigation: Install and run it only against Redis environments you control, with the UI bound to localhost. <br>


## Reference(s): <br>
- [ClawHub Redis Commander skill page](https://clawhub.ai/pereirajair/redis-commander) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local Docker lifecycle commands for a Redis Commander container.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
