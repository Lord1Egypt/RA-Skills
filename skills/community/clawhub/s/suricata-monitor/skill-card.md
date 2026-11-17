## Description:

Read and triage Suricata IDS/IPS alerts from eve.json into a structured threat report with severity-ranked findings, attacker IPs, top triggered signatures, and recommended blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infectit007](https://clawhub.ai/user/infectit007)

### License/Terms of Use:

MIT-0

## Use Case:

Security operators, system administrators, and developers use this skill to summarize recent Suricata IDS/IPS alerts into an actionable threat report for daily monitoring or post-scan review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suricata logs and generated threat reports may contain sensitive network, host, and alert details.

Mitigation: Treat logs and reports as sensitive, restrict access to generated report files, and avoid forwarding them outside approved channels.

Risk: The skill's local-only privacy claim conflicts with optional Telegram delivery, memory writes, and scheduled recurring execution.

Mitigation: Make Telegram delivery, memory writes, and cron scheduling explicit opt-in steps, and verify the destination and retention policy before enabling them.

Risk: Using chmod 644 on /var/log/suricata/eve.json can broaden access to security telemetry.

Mitigation: Prefer group membership or ACL-based log access that grants the agent only the permissions it needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/infectit007/skills/suricata-monitor)
- [Publisher profile](https://clawhub.ai/user/infectit007)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown threat report with inline shell commands and optional Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes recent local Suricata eve.json alert records by severity, source IP, signature, and GREEN/YELLOW/RED status.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
