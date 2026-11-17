## Description:

Audit and harden an OpenClaw host and its network exposure. Use for security checks, hardening, firewall setup, network exposure review, metrics endpoint restriction, OpenClaw gateway security fixes, or step-by-step remediation on a Linux host running OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimpang8](https://clawhub.ai/user/jimpang8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit and harden Linux hosts running OpenClaw, review network exposure, apply firewall rules with explicit approval, and verify gateway and security state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Firewall or network-hardening changes could interrupt remote management access on an OpenClaw Linux host.

Mitigation: Review and explicitly approve sudo, UFW, chmod, and /etc/ufw rollback actions; add management-access rules before enabling restrictive firewall policy.

Risk: Broad metrics, dashboard, remote desktop, or gateway exposure could remain if findings are applied generically.

Mitigation: Use exact host findings, approved source IPs or subnets, and post-change verification with OpenClaw audit, gateway status, UFW status, and listening-port checks.

## Reference(s):

- [OpenClaw Fix Patterns](references/openclaw-fix-patterns.md)
- [UFW Playbook](references/ufw-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, JSON configuration examples, and shell script snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate firewall-rules.md, apply-firewall.sh, scripts/rollback-firewall.sh, and scripts/verify-firewall.sh when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
