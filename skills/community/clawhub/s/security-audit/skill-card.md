## Description:

Comprehensive security auditing for Clawdbot deployments. Scans for exposed credentials, open ports, weak configs, and vulnerabilities. Auto-fix mode included.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chandrasekar-r](https://clawhub.ai/user/chandrasekar-r)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to audit Clawdbot deployments before release or on a recurring schedule, checking credentials, ports, configuration, file permissions, Docker settings, and Git exposure. It can also generate a JSON audit report or apply automatic remediation for some common findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive Clawdbot configuration and project files while scanning for credentials and weak settings.

Mitigation: Run it only in an environment where reading Clawdbot secrets and files under /root/clawd is acceptable.

Risk: Auto-fix mode can broadly change permissions on JSON, env, key, and PEM files.

Mitigation: Avoid running --fix as root or on production systems unless backups exist and recursive permission changes are acceptable.

Risk: Security evidence marks the release as suspicious because the audit behavior is plausible but broad in filesystem access and remediation scope.

Mitigation: Review the skill before installing and prefer read-only audit modes until the operational impact is understood.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text audit report with optional JSON report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May set a non-zero process exit code when critical findings are detected.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-01-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
