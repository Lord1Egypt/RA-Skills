## Description: <br>
Audits local OpenClaw configuration files for vulnerabilities in network settings, channel policies, and tool permissions, then produces safe remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoowii](https://clawhub.ai/user/zoowii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security reviewers use this skill to audit OpenClaw deployments after setup, before production exposure, after configuration changes, or during periodic security checks. It analyzes local configuration and reports findings with remediation steps and rollback guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may expose hostname, configuration paths, and details about the deployment's security posture. <br>
Mitigation: Treat reports as sensitive operational security material, store them with restricted access, and redact environment-specific details before sharing. <br>
Risk: Remediation steps may break remote access or existing workflows when applied directly to production configuration. <br>
Mitigation: Review recommendations before applying them, back up configuration files, verify alternate access, and use staged rollout with rollback procedures for higher-risk changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zoowii/scanner-for-openclaw) <br>
- [OpenClaw Security Scanner Homepage](https://github.com/openclaw/openclaw/tree/main/skills/openclaw-security-scanner) <br>
- [Permission Management](references/permission-management.md) <br>
- [Remediation Playbook](references/remediation-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, configuration guidance, shell commands] <br>
**Output Format:** [Markdown audit report with findings, risk levels, remediation steps, rollback plans, and command-line status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a Markdown report file such as security_report_*.md to the workspace.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
