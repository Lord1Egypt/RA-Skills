## Description: <br>
Web Security Audit Skills scans PHP, Java, Python, and Go web application code with regex-based rules and generates Security.md reports with findings, remediation guidance, and PoC examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moxin1044](https://clawhub.ai/user/moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan authorized web application codebases for common vulnerability patterns and produce a structured Security.md audit report with findings and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Security.md reports can include runnable exploit scripts for vulnerabilities such as RCE, SSRF, file-read, and webshell upload. <br>
Mitigation: Use the skill only on code and systems you are authorized to assess, review generated reports before sharing or committing them, and do not run generated PoCs against live targets without explicit permission and containment. <br>
Risk: Regex-based static analysis may report false positives or miss vulnerabilities that require deeper data-flow analysis. <br>
Mitigation: Treat findings as triage input, verify results manually, and pair the report with established secure code review or testing practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moxin1044/web-security-audit-skills) <br>
- [Publisher profile](https://clawhub.ai/user/moxin1044) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown Security.md report with optional JSON summary and inline Python PoC code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Security.md to the selected output path and may write a JSON summary when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
