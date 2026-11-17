## Description:

Performs local network scans using Nmap to detect vulnerabilities, identify service versions, and fingerprint operating systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacqueslauren](https://clawhub.ai/user/jacqueslauren)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to run authorized Nmap-based assessments of hosts or network ranges and review structured results for services, versions, operating system fingerprints, and vulnerability findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch active Nmap scans against arbitrary targets without strong scope controls or target validation.

Mitigation: Use it only on systems and networks you own or are explicitly authorized to test, and require target validation or manual confirmation before scanning hostnames, CIDR ranges, or user-supplied target text.

Risk: Nmap vulnerability, service, and OS scans can be intrusive or legally sensitive outside an approved testing scope.

Mitigation: Confirm written authorization, scan scope, timing, and required permissions before enabling or running scans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacqueslauren/skills/tech-security-audit)
- [Publisher profile](https://clawhub.ai/user/jacqueslauren)
- [Artifact README](artifact/README.md)
- [Artifact skill overview](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and Python dictionary results parsed from Nmap XML output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Nmap in PATH; scan execution can take up to 300 seconds before timeout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
