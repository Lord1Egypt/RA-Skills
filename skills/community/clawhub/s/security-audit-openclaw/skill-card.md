## Description: <br>
Performs comprehensive local security auditing for OpenClaw deployments, using system-level inspection to generate a brief summary and a detailed report while keeping core scans read-only and local-only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iaadoa](https://clawhub.ai/user/iaadoa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and administrators use this skill to audit OpenClaw systems they own or administer for misconfiguration, exposure, credential leakage, file integrity drift, cron and SSH posture, and recovery readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs high-privilege local security inspection and may expose sensitive system posture in generated reports. <br>
Mitigation: Install and run it only on OpenClaw systems you own or administer, review reports before sharing them, and delete old /tmp audit reports if they contain sensitive findings. <br>
Risk: Optional Git backup or Telegram notification features can contact external services when enabled. <br>
Mitigation: Leave these features disabled unless explicitly needed, and enable them only after confirming the repository, remote, chat, and notification destination are intended. <br>
Risk: Scheduled audit runs can repeatedly create local reports that accumulate security-sensitive findings. <br>
Mitigation: Use cron scheduling only after confirming the cadence is appropriate and periodically manage report retention in /tmp/openclaw-security-reports/. <br>


## Reference(s): <br>
- [Security Declaration](SECURITY.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/iaadoa/security-audit-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples, stdout security brief, and plain-text audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Detailed reports are written under /tmp/openclaw-security-reports/ and may contain sensitive security findings.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
