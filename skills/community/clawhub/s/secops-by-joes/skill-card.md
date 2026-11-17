## Description:

SecOps checks for endpoints: EDR, Sysmon, updates, EVTX on heartbeat, least privilege, network visibility, credential protection (Kerberos/NTLM/pass-the-hash), device inventory and known vulnerabilities, weekly assessment, and skill integrity (hash-on-wake, version-aware).

This skill is ready for commercial/non-commercial use.

## Publisher:

[inaor](https://clawhub.ai/user/inaor)

### License/Terms of Use:

MIT

## Use Case:

Security analysts, SecOps engineers, and agent developers use this skill to assess Windows endpoint posture, review endpoint telemetry requirements, harden credential and privilege controls, and produce weekly host security assessments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to perform broad endpoint and network reconnaissance without a clear mandatory approval boundary.

Mitigation: Before use, define authorized hosts, data categories, and recurring checks, and require approval before collecting administrator membership, domain trust, session, Wi-Fi, neighbor, installed-software, vulnerability, or personal skill-directory integrity data.

Risk: The security scan verdict is suspicious because endpoint assessment and recurring integrity checks may expose sensitive operational data if run too broadly.

Mitigation: Use the skill only for authorized Windows endpoint-security assessments and keep generated reports limited to security-relevant summaries rather than raw logs, full inventories, or personal data.

## Reference(s):

- [Security Joes](https://www.securityjoes.com)
- [Security Joes About](https://www.securityjoes.com/about)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and structured endpoint posture fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compact host posture or weekly assessment reports using counts, booleans, event IDs, timestamps, and short summaries.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
