## Description: <br>
Scans code for common vulnerability patterns, including SQL injection, cross-site scripting, hardcoded secrets, insecure randomness, command injection, and sensitive information leaks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HonestQiao](https://clawhub.ai/user/HonestQiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill for lightweight checks of code snippets and small changes before deeper review. It returns vulnerability hints, severity information, line numbers, and a security score to guide remediation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regex-based scanning can miss vulnerabilities or flag benign code. <br>
Mitigation: Treat findings as review prompts and validate important issues with manual review or dedicated security tooling. <br>
Risk: Code samples may contain real secrets or sensitive information. <br>
Mitigation: Avoid submitting real credentials or confidential code unless intentional and permitted for inspection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HonestQiao/security-vuln-scanner) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/HonestQiao) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON and concise remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Regex-based findings should be treated as hints rather than a complete security audit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
