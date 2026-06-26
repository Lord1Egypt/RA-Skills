## Description: <br>
Monitor host system health (Disk, RAM, CPU). Returns structured JSON status for predictive maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[numbpill3d](https://clawhub.ai/user/numbpill3d) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to let an agent run a local host health check and report disk, memory, and CPU load status before resource exhaustion causes failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local disk, memory, and CPU load metrics may be sensitive if exposed in agent output or logs. <br>
Mitigation: Use this skill only where host health metrics are permitted to be collected and logged, and avoid sharing outputs outside approved operational contexts. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/numbpill3d/system-vigil) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands] <br>
**Output Format:** [JSON object printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports overall status, disk usage percent, memory usage percent, 15-minute load average, and warnings.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
