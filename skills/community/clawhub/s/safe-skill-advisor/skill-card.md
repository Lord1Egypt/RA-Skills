## Description: <br>
Security Skill Advisor - Protect you from malicious skills on ClawHub. Provides security warnings, tool recommendations, and 30-second self-check checklist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crystaria](https://clawhub.ai/user/crystaria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill before installing ClawHub skills to review common red flags, choose scanner tools, and decide how to report or clean up suspicious skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation language may cause the advisor to apply security guidance to conversations where the user's intent is unclear. <br>
Mitigation: Use the skill as checklist guidance and ask clarifying questions before applying recommendations to a specific skill or install decision. <br>
Risk: The skill recommends external scanner tools that users may install separately. <br>
Mitigation: Verify the publisher, source repository, and package integrity for third-party tools before installing or running them. <br>
Risk: Cleanup workflows can involve command history, process lists, or network output that may contain secrets. <br>
Mitigation: Review and redact sensitive values before sharing diagnostic output with another person or service. <br>


## Reference(s): <br>
- [Safe Skill Advisor on ClawHub](https://clawhub.ai/skills/safe-skill-advisor) <br>
- [Safe Skill Advisor release page](https://clawhub.ai/crystaria/safe-skill-advisor) <br>
- [Cisco AI Skill Scanner](https://github.com/cisco-ai-skill-scanner) <br>
- [SecureClaw](https://github.com/adversa-ai/secureclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline shell commands, checklists, and short remediation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only advisor; it does not execute scans or modify files by itself.] <br>

## Skill Version(s): <br>
1.7.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
