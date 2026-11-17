## Description:

Reports local disk usage, kernel and operating system details, uptime, and load by running df, uname, and uptime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aneasystone](https://clawhub.ai/user/aneasystone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to answer quick questions about the current host's disk usage, OS and kernel version, uptime, and load. It is intended for read-only local system status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may reveal local system details such as disk usage, kernel and OS information, uptime, and load.

Mitigation: Use it only where sharing host status with the agent is acceptable, and avoid installing it in environments where these details are sensitive.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text with command lines and short summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports command output from df, uname, and uptime; no file writes or elevated privileges are requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
