## Description: <br>
Rafter Security helps agents and developers scan code, audit skills and agent configurations, classify shell-command risk, and generate security review guidance with the Rafter CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafter](https://clawhub.ai/user/rafter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and agent users use this skill to run Rafter security checks, audit third-party skills and agent configurations before installation, evaluate shell commands, and generate security review questions for new features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API-backed Rafter scans may send code or findings to Rafter services when RAFTER_API_KEY is configured. <br>
Mitigation: Use local-only scans when remote analysis is not appropriate, and configure RAFTER_API_KEY only after confirming the service is trusted for the code being reviewed. <br>
Risk: Rafter agent initialization may add hooks or logging that affect future command execution. <br>
Mitigation: Review selected opt-in integrations before running initialization, and inspect resulting agent configuration and audit logs after setup. <br>
Risk: The skill depends on the external rafter CLI. <br>
Mitigation: Install the CLI from a trusted source and verify it is acceptable for the target environment before using the skill. <br>


## Reference(s): <br>
- [Rafter Security on ClawHub](https://clawhub.ai/rafter/skills/rafter-security) <br>
- [Rafter](https://rafter.so) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and structured security findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference the RAFTER_API_KEY environment variable for API-backed scans; local secrets scans can run without it.] <br>

## Skill Version(s): <br>
0.8.10 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
