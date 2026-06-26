## Description: <br>
Security-first skill vetting for AI agents. Use BEFORE installing any skill from ClawHub, GitHub, or other sources. Checks for red flags, dangerous patterns, permission scope, and suspicious code. Protects the agent and user from malicious skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MissCrx](https://clawhub.ai/user/MissCrx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to review external skills before installation, scan for critical security red flags, and decide whether flagged behavior needs manual review or blocking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated regex-based scanning may miss malicious behavior or flag benign patterns. <br>
Mitigation: Use the skill as a vetting aid and manually review flagged files, commands, and context before installing a reviewed skill. <br>
Risk: Scanner reports may include file paths or code snippets from the reviewed skill. <br>
Mitigation: Run the scanner only against the intended skill directory and inspect reports before sharing them. <br>


## Reference(s): <br>
- [Security Pattern Reference](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional scanner reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner output groups findings into critical issues, warnings, informational notes, boundary findings, and an overall recommendation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
