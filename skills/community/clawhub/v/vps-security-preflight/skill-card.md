## Description:

Run and interpret a read-only OpenClaw security preflight on an authorized Linux VPS. Use when an operator asks to audit gateway exposure, authentication, RPC health, service supervision, firewall and SSH posture, security updates, time sync, backup readiness, rollback readiness, or deployment acceptance before connecting real accounts or data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinyopsstudio](https://clawhub.ai/user/tinyopsstudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and site reliability engineers use this skill to run a read-only OpenClaw VPS security audit and summarize the highest-priority remediation steps before connecting real accounts or data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local audit commands on an authorized VPS and may expose host configuration or security posture details in the output.

Mitigation: Run it only on authorized Linux VPS hosts and review or redact output before sharing, especially when using the optional raw deep-audit mode.

Risk: The audit is a conservative preflight and does not prove full-system security, backup freshness, restore readiness, spend limits, or rollback readiness.

Mitigation: Treat failures as blockers, manually verify controls that the script reports as informational, and compare recommendations with current OpenClaw security documentation.

Risk: Remediation guidance could lead to configuration changes outside the read-only audit scope.

Mitigation: Get explicit operator approval before changing firewall rules, authentication, packages, ports, services, or deployment configuration.

## Reference(s):

- [OpenClaw security documentation](https://docs.openclaw.ai/gateway/security)
- [ClawHub skill release page](https://clawhub.ai/tinyopsstudio/skills/vps-security-preflight)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with inline shell commands and PASS/WARN/FAIL/INFO audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Raw deep-audit output is optional and should be reviewed and redacted before sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
