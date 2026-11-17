## Description:

Autonomous VPS monitoring and auto-remediation - kills runaway processes, frees disk, restarts dead services, and hardens security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strouddustinn-bot](https://clawhub.ai/user/strouddustinn-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to monitor Linux VPS hosts and propose or run remediation for runaway processes, disk pressure, failed services, memory pressure, and basic SSH abuse signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run high-impact root-level remediation on a VPS.

Mitigation: Review carefully before installing, require explicit approvals, and define backups and rollback plans before enabling remediation.

Risk: The documented sudo curl installation path has weak reviewability unless the downloaded payload is pinned and verified.

Mitigation: Avoid the sudo curl path unless the payload hash and source are pinned and verified before execution.

Risk: Daemon or cron mode can repeatedly kill processes, clean files, restart services, drop caches, or alter firewall behavior.

Mitigation: Start in dry-run mode, avoid daemon or cron mode on production hosts until reviewed, and use allowlists for services, processes, and firewall changes.

## Reference(s):

- [VPS Guardian documentation](https://vps-guardian.io/docs)
- [VPS Guardian issues](https://github.com/vps-guardian/guardian/issues)
- [ClawHub skill page](https://clawhub.ai/strouddustinn-bot/skills/vps-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run guidance, service and process remediation steps, and host configuration recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
