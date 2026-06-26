## Description: <br>
YES.md 中文版 is a Chinese engineering workflow skill that guides agents to gather evidence, verify changes, avoid unsupported assumptions, and check downstream impact during development, debugging, configuration, deployment, API integration, and data work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sstklen](https://clawhub.ai/user/sstklen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to stay evidence-driven during file edits, configuration changes, deployments, debugging, API integration, and data-processing tasks. It is intended to make agents verify claims, use available tools before asking the user, back up risky files, and perform follow-up checks after changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages tool use and evidence gathering during engineering work, which can include commands that inspect production, database, deployment, or sensitive environment details. <br>
Mitigation: Keep normal approval controls for production deployments, database changes, and commands that read sensitive environment details. <br>
Risk: The skill is broad workflow guidance, so applying it mechanically to every task could add unnecessary backups, checks, or command execution. <br>
Mitigation: Use it for engineering changes, debugging, configuration, deployment, API integration, and data work where evidence gathering and verification reduce risk. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline command and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; it does not include executable code or credential handling.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
