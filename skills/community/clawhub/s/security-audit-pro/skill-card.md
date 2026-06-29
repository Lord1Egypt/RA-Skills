## Description: <br>
Security Audit Pro guides agents through security reviews covering static code analysis, dependency vulnerabilities, container security, cloud configuration compliance, secret leakage, network exposure, permission review, and prioritized remediation reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and platform teams use this skill to review codebases, dependencies, containers, cloud configurations, secrets, network exposure, and permissions, then produce a prioritized remediation report. It is intended to support technical security assessment and compliance preparation, not replace a formal audit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive project, dependency, container, or cloud configuration context. <br>
Mitigation: Use scoped targets and avoid sharing production credentials unless the audit task requires them. <br>
Risk: Security scanner results and static-analysis findings can include false positives. <br>
Mitigation: Have a qualified reviewer confirm findings before remediation or compliance decisions. <br>
Risk: Detected secret exposure may indicate active credential risk. <br>
Mitigation: Rotate and revoke exposed credentials promptly when leakage is confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/security-audit-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown security audit report with prioritized findings and remediation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on user-provided scanner outputs, project context, and scoped security credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
