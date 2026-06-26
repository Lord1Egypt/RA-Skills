## Description: <br>
Sentinel- OpenClaw Runtime Security provides runtime security monitoring for OpenClaw agents, including skill integrity checks, prompt injection detection, credential exposure auditing, and optional premium daemon, egress, and process anomaly monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spaceman420urdog-afk](https://clawhub.ai/user/spaceman420urdog-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security-conscious OpenClaw users use this skill to audit installed skills, check new skills before installation, and monitor runtime behavior for suspicious file, prompt, credential, network, or process activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local security binary that reads OpenClaw skill files and can monitor process and network activity in daemon mode. <br>
Mitigation: Install only if this monitoring behavior is acceptable, review findings before action, and use --offline for local-only scans when remote calls are not needed. <br>
Risk: Premium features store wallet keys locally and may auto-sign small USDC payments. <br>
Mitigation: Set the wallet spend limit to 0 before funding it, confirm payment details before enabling auto-approval, and export or back up recovery material carefully. <br>
Risk: Remote ClawHub checks and payment recipient validation were flagged for caution by the security guidance. <br>
Mitigation: Prefer local-path checks and avoid remote checks until archive extraction and payment recipient validation are tightened. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spaceman420urdog-afk/runtime-sentinel) <br>
- [Threat model](references/threat-model.md) <br>
- [x402 payment flow](references/x402-payment.md) <br>
- [Binary build guide](references/binary-build.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured CLI reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a local Rust CLI that reads OpenClaw skill files and produces risk reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
