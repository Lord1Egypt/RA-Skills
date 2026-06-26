## Description: <br>
Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a-din](https://clawhub.ai/user/a-din) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to review third-party skills before installation, checking source, permission scope, suspicious patterns, and risk level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example shell commands may fetch data from repositories that are not the intended review target. <br>
Mitigation: Run commands only against repositories you intend to inspect and verify the repository owner, name, and skill path before using fetched content. <br>
Risk: Checklist guidance may be over-relied on for high-risk skills or skills requesting sensitive access. <br>
Mitigation: Treat the skill as a review aid and require human approval for skills involving credentials, privileged access, external data transfer, or system-level changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/a-din/xiaopi-skill-vetter) <br>
- [Publisher profile](https://clawhub.ai/user/a-din) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown checklist and vetting report with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review guidance only; it does not include executable skill code.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
