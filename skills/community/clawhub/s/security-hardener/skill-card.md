## Description: <br>
One-command OpenClaw security audit, scoring, and auto-remediation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit and harden OpenClaw installations before deployment or exposure. It checks authentication, transport, secrets, file permissions, plugin posture, network exposure, and known OpenClaw CVEs, then reports findings or applies supported fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect sensitive local configuration, environment, memory, shell history, and git-history content while looking for exposed secrets. <br>
Mitigation: Run it only in an environment where that local inspection is intended, review generated findings before sharing reports, and keep any reports containing secrets private. <br>
Risk: The fix workflow can change file permissions, move discovered keys to environment files, alter authentication settings, bind OpenClaw to localhost, and disable unsigned plugins. <br>
Mitigation: Use audit mode or fix --dry-run first, review the planned changes, and rely on the timestamped backup before applying fixes. <br>


## Reference(s): <br>
- [Security Hardener ClawHub Page](https://clawhub.ai/stevojarvisai-star/security-hardener) <br>
- [CVE Database - OpenClaw Security](references/cve-database.md) <br>
- [GetAgentIQ](https://getagentiq.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON, and shell command guidance depending on the selected command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce security scores, severity-ranked findings, remediation recommendations, dry-run previews, and markdown reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
