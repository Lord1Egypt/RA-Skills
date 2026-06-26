## Description: <br>
Comprehensive security auditing for Clawdbot deployments. Scans for exposed credentials, open ports, weak configs, and vulnerabilities. Auto-fix mode included. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianjin-ren](https://clawhub.ai/user/tianjin-ren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit Clawdbot deployments under /root/clawd for exposed credentials, open ports, weak configuration, file-permission issues, Docker risks, and related deployment concerns. They can run a normal audit first, generate a private JSON report, and use the explicit auto-fix mode only for reviewed common fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports may expose sensitive paths or credential locations. <br>
Mitigation: Keep reports private and share them only with people responsible for the Clawdbot deployment. <br>
Risk: Auto-fix mode can change permissions on .env, JSON, key, and PEM files and create a .gitignore. <br>
Mitigation: Run the normal audit first and review or back up configuration files before invoking --fix. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianjin-ren/security-audit-tianjin) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with optional JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Auto-fix mode can update local file permissions and create a .gitignore after user invocation.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
