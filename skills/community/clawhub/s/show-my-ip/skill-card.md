## Description:

Show the current public IP address of the server. Use when asked about IP, public IP, or network identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericsantos](https://clawhub.ai/user/ericsantos)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to check the public network identity of the agent host for debugging, VPN verification, allowlisting, and firewall setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to ifconfig.me and displays the host's public IP address, which may be sensitive in privacy-conscious or enterprise environments.

Mitigation: Install only where public IP disclosure is acceptable; use an approved internal IP-reflection endpoint in controlled enterprise environments.

## Reference(s):

- [ifconfig.me](https://ifconfig.me)
- [ClawHub skill page](https://clawhub.ai/ericsantos/skills/show-my-ip)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with IPv4 and optional IPv6 lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and outbound HTTPS access to ifconfig.me; IPv4 is reported as unavailable if the request does not return a value.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
