## Description:

Runtime security guardian for OpenClaw agents that audits skill integrity, scans prompt injection and credential exposure, and can monitor file, network, and process activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spaceman420urdog-afk](https://clawhub.ai/user/spaceman420urdog-afk)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to check installed or candidate skills for runtime security issues, suspicious behavior, credential exposure, prompt injection, unexpected network egress, and process anomalies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Premium mode stores wallet material locally and may auto-sign small USDC payments.

Mitigation: Use offline/free mode when premium monitoring is not required, or set the payment limit to 0 so each payment requires explicit confirmation.

Risk: Daemon mode monitors local skill files and process/network activity and writes audit logs.

Mitigation: Review daemon logs for sensitive command-line arguments and run the daemon only in environments where that monitoring scope is acceptable.

Risk: The install flow can rely on downloaded or built binaries.

Mitigation: Verify binaries with an independently signed digest before installation and prefer building from reviewed source when appropriate.

Risk: The release has a server security verdict of suspicious.

Mitigation: Review the security summary and install only after accepting the payment, monitoring, logging, and binary trust implications.

## Reference(s):

- [Threat Model](references/threat-model.md)
- [x402 Payment Flow](references/x402-payment.md)
- [Building sentinel](references/binary-build.md)
- [x402 protocol](https://github.com/coinbase/x402)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text, with optional JSON reports from the sentinel CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk levels, findings, remediation commands, wallet setup guidance, daemon status, and audit log excerpts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
