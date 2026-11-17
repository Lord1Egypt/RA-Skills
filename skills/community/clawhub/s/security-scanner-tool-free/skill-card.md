## Description: <br>
安全扫描器(免费版) helps agents guide authorized security assessments with port scanning, vulnerability checks, SSL/TLS analysis, web server scanning, and Markdown report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers and developers use this skill to plan and run authorized local security scans, compare outputs from nmap, nuclei, sslscan, and nikto, and produce scan reports for assessment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger active network scanning against supplied targets. <br>
Mitigation: Use it only for assets you are authorized to test and validate targets before any command runs. <br>
Risk: The sample execution path interpolates user-supplied targets into shell commands with exec access. <br>
Mitigation: Replace shell=True and raw command strings with structured subprocess argument lists before running generated scripts or commands. <br>
Risk: Local scan reports may contain sensitive security findings. <br>
Mitigation: Store generated reports only in approved locations and handle them according to internal security data procedures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/security-scanner-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash and Python examples plus JSON-style result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local scan reports and command outputs that contain sensitive security findings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
