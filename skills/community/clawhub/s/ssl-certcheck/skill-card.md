## Description:

Check SSL/TLS certificates for hostnames, including expiry dates, issuer, subject alternative names, protocol version, and cipher suite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect SSL/TLS certificate health for public or internal hostnames, including expiry monitoring and TLS detail checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker opens outbound TLS connections to user-specified hostnames and ports, including internal hostnames if provided.

Mitigation: Run checks only against intended hosts and ports, and avoid submitting sensitive internal hostnames unless that network access is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogue-agent1/skills/ssl-certcheck)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with bash command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make outbound TLS connections to user-specified hostnames and ports when executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
