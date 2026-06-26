## Description: <br>
Captures vulnerabilities, misconfigurations, access control violations, compliance gaps, incident response patterns, and threat intelligence to enable continuous security improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and agent operators use this skill to record security findings, incidents, compliance gaps, remediation notes, and hardening requests in local learning files. It supports continuous improvement by turning repeated or broadly useful findings into security guidance, runbooks, checklists, or agent instructions after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security learning logs can accidentally preserve sensitive data if findings are copied without redaction. <br>
Mitigation: Redact secrets, tokens, keys, credentials, and PII before logging; store only the type, location, impact, and remediation details. <br>
Risk: Optional hooks and command-output scanning can add broad reminders or pattern checks in projects where that behavior is not wanted. <br>
Mitigation: Keep hooks disabled unless useful, prefer narrow security matchers, and enable command-output scanning only in trusted projects. <br>
Risk: Promoting findings into persistent agent guidance can introduce incorrect or misleading instructions if entries are not reviewed. <br>
Mitigation: Manually review and scan entries before promoting them into AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, runbooks, or reusable skills. <br>


## Reference(s): <br>
- [OpenClaw Security Integration](references/openclaw-integration.md) <br>
- [Hooks Setup](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [ClawHub release page](https://clawhub.ai/jose-compu/self-improving-security) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown entries, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local security learning files and may provide optional hook reminders when explicitly enabled.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
