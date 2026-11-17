## Description:

Monitor VPS and server health metrics including real-time CPU usage, RAM utilization, disk usage, and Docker container status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanjay-gthb](https://clawhub.ai/user/sanjay-gthb)

### License/Terms of Use:

MIT

## Use Case:

Developers, DevOps engineers, and system administrators use this skill to check VPS or server health, troubleshoot resource bottlenecks, and monitor containerized environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reveal host resource metrics and Docker container names or status to the requesting agent or logs.

Mitigation: Install it only in environments where those operational details may be shared, and limit Docker access when container visibility is not needed.

Risk: The skill requires shell permission to collect server health metrics.

Mitigation: Review and scan the release before deployment, and run it under the least-privileged account or container context that can provide the required read-only metrics.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes success status, skill name, timestamp, CPU percentage, RAM percentage, root filesystem disk usage, and Docker container status when available.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
