## Description: <br>
Monitors VPS and server health metrics including real-time CPU usage, RAM utilization, disk usage, and Docker container status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanjay-gthb](https://clawhub.ai/user/sanjay-gthb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, DevOps engineers, and system administrators use this skill to check server CPU, memory, disk, and Docker container health during monitoring and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes local host health metrics and Docker container names or statuses to the agent session. <br>
Mitigation: Install it only where OpenClaw is allowed to run local read-only health commands and view host and Docker status information. <br>
Risk: Health checks may be incomplete when local commands such as top, free, df, or docker are unavailable or restricted. <br>
Mitigation: Treat unavailable fields as an operational signal and cross-check critical incidents with the host's normal monitoring tools. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports point-in-time CPU, RAM, disk usage, Docker status, timestamp, and success or error fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
