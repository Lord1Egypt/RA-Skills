## Description: <br>
OpenClaw repair toolkit for automated diagnostics, backup and restore, and guided AI-assisted recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amrree](https://clawhub.ai/user/amrree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to diagnose startup, gateway, configuration, network, and API-key problems, back up and restore OpenClaw state, and request local Ollama repair guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The toolkit can make high-impact local changes, including installing software, starting or stopping OpenClaw, clearing logs, and resetting or restoring session data. <br>
Mitigation: Run diagnostics first, inspect the scripts before repair or reset paths, and execute destructive recovery commands only after confirming the intended backup or restore target. <br>
Risk: Backup behavior can copy a GitHub token into the backup directory. <br>
Mitigation: Avoid backing up secrets unless the backup location is encrypted and access-restricted, and remove or rotate copied tokens when they are no longer needed. <br>
Risk: The artifact includes an installer path that pipes a remote Ollama install script into the shell. <br>
Mitigation: Verify installer contents independently or install dependencies through a trusted package manager before running AI-assisted repair setup. <br>


## Reference(s): <br>
- [SolCal Recovery on ClawHub](https://clawhub.ai/amrree/skills/solcal-recovery) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Ollama install documentation](https://ollama.ai/install) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local backup files and restore OpenClaw configuration, sessions, skills, and selected secrets when the included scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
