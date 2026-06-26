## Description: <br>
Installs, updates, lists, imports, and removes remote OpenClaw skills for selected agent workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ysy88092144](https://clawhub.ai/user/ysy88092144) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install, update, remove, and bulk-import skills into local agent workspaces from remote URLs or configured skill hubs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently install or overwrite local agent skills from remote URLs and mirrors without strong source verification or overwrite confirmation. <br>
Mitigation: Install only from trusted HTTPS sources, review downloaded SKILL.md files before enabling them, and back up OpenClaw workspaces before import, update, or remove operations. <br>
Risk: Remote skill installation can change future agent behavior in ways that are not obvious from the command invocation alone. <br>
Mitigation: Review the installed skill content and recorded source metadata after installation, then remove unexpected or untrusted skills before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ysy88092144/remote-skill-installer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local filesystem changes under OpenClaw workspaces and remote source metadata recorded for installed skills.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
