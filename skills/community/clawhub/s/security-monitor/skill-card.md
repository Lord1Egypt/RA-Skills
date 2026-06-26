## Description: <br>
Real-time security monitoring for Clawdbot. Detects intrusions, unusual API calls, credential usage patterns, and alerts on breaches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chandrasekar-r](https://clawhub.ai/user/chandrasekar-r) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run continuous security monitoring on a Clawdbot deployment, including failed-login, port, process, file-change, API-credential, and Docker health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports access to local auth logs, port and process listings, Docker status, /root/clawd paths, and /root/clawd/skills/.env. <br>
Mitigation: Install only if that local access is acceptable, run with the least privilege needed for the checks you use, and review the script before deployment. <br>
Risk: The security review reports a credential-file check and generated log and state files that may need protection. <br>
Mitigation: Review or patch credential-file handling, protect generated files, and rotate credentials if sensitive data is exposed. <br>
Risk: The security review reports that advertised --threats scoping is nonfunctional. <br>
Mitigation: Do not rely on --threats to narrow monitoring until it is patched; assume all checks may run. <br>


## Reference(s): <br>
- [Security Monitor on ClawHub](https://clawhub.ai/chandrasekar-r/security-monitor) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Console text and newline-delimited JSON log entries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run once or continuously in daemon mode; writes alert and state files under /root/clawd/clawdbot-security.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
