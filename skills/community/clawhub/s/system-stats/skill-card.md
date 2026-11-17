## Description:

Reports real-time local system performance metrics including CPU, memory, swap, network throughput, disk I/O, system load, and process count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support agents use this skill to inspect local host performance during troubleshooting or capacity checks from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill prints local machine performance details that may be sensitive in shared logs.

Mitigation: Run it only in trusted sessions and avoid storing or sharing outputs that expose host resource usage.

Risk: The skill depends on psutil from the Python environment.

Mitigation: Use a virtual environment and pin psutil to a reviewed version before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text system metric report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts an optional CPU sampling interval in seconds and requires psutil in the execution environment.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
