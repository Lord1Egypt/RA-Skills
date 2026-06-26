## Description: <br>
Manage OpenClaw Skills by listing, checking updates, installing, updating, or uninstalling from GitHub, SkillHub, Config, or local sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy8663](https://clawhub.ai/user/andy8663) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect installed skills, check for available updates, install or update skills, and remove skills from local OpenClaw locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uninstall behavior may remove installed skills, configuration files, or related local state. <br>
Mitigation: Back up installed skills and configuration files, review the target paths, and use dry-run mode before uninstalling. <br>
Risk: The script contains hard-coded local Windows OpenClaw paths. <br>
Mitigation: Replace the hard-coded paths with the user's actual OpenClaw paths before running management commands. <br>
Risk: The security review flags the release as suspicious because uninstall behavior and local path handling need review. <br>
Mitigation: Install only after reviewing or fixing the script, and avoid preserve-related uninstall behavior until config-file deletion is corrected. <br>


## Reference(s): <br>
- [Skill Manage on ClawHub](https://clawhub.ai/andy8663/skill-manage) <br>
- [Publisher profile: andy8663](https://clawhub.ai/user/andy8663) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local file-management commands for OpenClaw skill directories when invoked by the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
