## Description: <br>
SentiClaw helps OpenClaw developers add runtime checks for prompt injection, identity spoofing, PII leakage, outbound data exposure, rate limiting, audit logging, and threat alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SuperTechGod](https://clawhub.ai/user/SuperTechGod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use SentiClaw to add inbound and outbound runtime guardrails, PII redaction, audit logging, and alerting around agent workflows. It is intended for AI-layer hardening and monitoring, not network or firewall security. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit records can contain security-event details plus session, sender, and channel identifiers. <br>
Mitigation: Use a protected audit_db_path, restrict file permissions, rotate or purge logs as needed, or disable auditing when local retention is not acceptable. <br>
Risk: Configured threat alerts can send session and sender identifiers to external messaging channels. <br>
Mitigation: Configure alerts only for private approved channels and review channel membership before enabling alert_channel_id. <br>
Risk: The path-check helper may allow broader local paths than intended if allowed_dirs is left at the default. <br>
Mitigation: Narrow allowed_dirs to the minimum directories required by the agent workflow. <br>
Risk: SentiClaw is AI-layer middleware and is not a network or firewall security control. <br>
Mitigation: Use it as one control in a broader security program rather than the only enforcement layer. <br>


## Reference(s): <br>
- [SentiClaw on ClawHub](https://clawhub.ai/SuperTechGod/senticlaw) <br>
- [SuperTechGod publisher profile](https://clawhub.ai/user/SuperTechGod) <br>
- [PHRAIMWORK LLC](https://phraimwork.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python API results, Markdown instructions, inline shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local SQLite audit records and send configured security alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md metadata, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
