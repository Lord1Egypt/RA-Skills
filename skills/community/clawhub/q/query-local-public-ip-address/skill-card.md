## Description:

Retrieves the local machine's current public IP address by running a Python script that queries public IP lookup services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangensure](https://clawhub.ai/user/zhangensure)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill when they need an agent to check and report the local machine's public IP address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts third-party public IP lookup services to determine the machine's public IP address.

Mitigation: Install and run it only where that outbound network contact is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangensure/skills/query-local-public-ip-address)
- [Publisher profile](https://clawhub.ai/user/zhangensure)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text public IP output, with concise Markdown guidance when used by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8 or higher and outbound HTTPS access to public IP lookup services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
