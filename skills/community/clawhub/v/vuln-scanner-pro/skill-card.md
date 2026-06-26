## Description: <br>
AI 代码安全审查 scans code for security vulnerabilities, injection risks, unsafe configuration, and related remediation guidance using OWASP and CWE-oriented rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to submit code for automated security review, receive structured vulnerability findings, and prioritize fixes before deployment or during code audit workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence marks the skill as suspicious because it sends source code and payment credentials to a plain-HTTP IP address without privacy or retention disclosure. <br>
Mitigation: Review carefully before installing, remove secrets before use, and avoid proprietary or sensitive repositories unless the publisher provides HTTPS and clear data-handling terms. <br>
Risk: The skill requires payment credentials for a paid remote scanning workflow. <br>
Mitigation: Use only credentials intended for this service, verify the publisher and endpoint before payment, and avoid sharing reusable or unrelated payment tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/vuln-scanner-pro) <br>
- [security-scan.json](references/security-scan.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Structured JSON or Markdown security review reports with vulnerability summaries, CWE and OWASP references, severity details, scores, and remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include line-level findings, service tier information, security scores, and suggested code changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
