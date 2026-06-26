## Description: <br>
Dispatches scheduled workload tasks to worker nodes for execution and records dispatch logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink5725](https://clawhub.ai/user/ink5725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to turn scheduler output into dispatch records for worker-node execution, monitoring, auditing, and failure recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script writes dispatch records to an absolute log directory when executed. <br>
Mitigation: Run it only in environments where /var/log/compute/dispatched is the intended dispatch log location and permissions are scoped to that path. <br>
Risk: The security guidance flags high-authority workflow expectations for installation. <br>
Mitigation: Install only when this operational dispatch behavior is expected, and review any account, repository, or deployment actions before approving them. <br>


## Reference(s): <br>
- [Task Dispatcher on ClawHub](https://clawhub.ai/ink5725/task-dispatche) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files] <br>
**Output Format:** [JSON object with dispatch metadata and per-task JSON dispatch log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dispatch records under /var/log/compute/dispatched when the bundled script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
