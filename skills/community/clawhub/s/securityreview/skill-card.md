## Description: <br>
Conducts source-code security reviews focused on concrete vulnerabilities such as hardcoded secrets, access control flaws, insecure data handling, injection risks, authentication weaknesses, LLM safety issues, and privacy violations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylehuan](https://clawhub.ai/user/kylehuan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to guide agent-assisted source-code audits and produce actionable reports for vulnerabilities that can be fixed in the reviewed code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review reports and optional .shield_security/ artifacts may expose real vulnerabilities, file paths, or secrets found during review. <br>
Mitigation: Install only for repositories the agent is allowed to inspect, treat generated reports as sensitive, and restrict sharing to appropriate reviewers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kylehuan/securityreview) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown security report with vulnerability findings, severity, source locations, impact descriptions, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scoped local report artifacts under .shield_security/ when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
