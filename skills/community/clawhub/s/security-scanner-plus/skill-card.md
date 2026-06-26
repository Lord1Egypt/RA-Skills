## Description: <br>
Scans AI agent skills for dependency vulnerabilities, dangerous code patterns, and undeclared permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennyzir](https://clawhub.ai/user/kennyzir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and marketplace operators use this skill to scan agent skills or code submissions for dependency vulnerabilities, risky code patterns, and undeclared permissions before installation, publishing, or CI deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan inputs may be sent to the Claw0x remote API. <br>
Mitigation: Only submit code, repositories, or skill data that you are authorized to send to Claw0x, and avoid private or regulated code unless your organization approves that processing. <br>
Risk: The skill requires a Claw0x API key. <br>
Mitigation: Use a dedicated, revocable CLAW0X_API_KEY stored in an environment variable or secret manager. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kennyzir/security-scanner-plus) <br>
- [Claw0x](https://claw0x.com) <br>
- [OSV.dev vulnerability database](https://osv.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON risk report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes risk level, risk score, dependency findings, code findings, permission audit results, recommendations, scan timestamp, and duration.] <br>

## Skill Version(s): <br>
1.0.7 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
