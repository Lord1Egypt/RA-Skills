## Description: <br>
Comprehensive security auditing for Clawdbot deployments. Scans for exposed credentials, open ports, weak configs, and vulnerabilities. Auto-fix mode included. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chandrasekar-r](https://clawhub.ai/user/chandrasekar-r) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to audit Clawdbot deployments before release or on a recurring schedule. It helps identify exposed credentials, unexpected ports, weak configuration, unsafe permissions, and Docker security issues, with an optional auto-fix mode for common problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports may expose local paths and details about the deployment security posture. <br>
Mitigation: Treat generated reports as sensitive operational security material and limit sharing to trusted reviewers. <br>
Risk: Auto-fix mode can modify file permissions and create a .gitignore file. <br>
Mitigation: Run the normal audit first, review the proposed remediation path, and use --fix only after confirming backups or version control recovery are available. <br>
Risk: The audit script reads local deployment files and uses local system tools. <br>
Mitigation: Run it only in the intended Clawdbot environment and review findings before acting on deployment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chandrasekar-r/security-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; optional plain text or JSON audit reports from the audit script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The audit may return a nonzero exit status when critical findings are detected. Auto-fix mode can change file permissions and create a .gitignore file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
