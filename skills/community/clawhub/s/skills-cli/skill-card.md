## Description: <br>
High-level helper for managing agent skills using the ClawHub CLI and local skill folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlang-cn](https://clawhub.ai/user/openlang-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to choose the right ClawHub CLI workflow for searching, installing, updating, publishing, syncing, and organizing agent skills in local skill folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk update, sync, or publish commands can affect multiple skill folders or publish unintended material. <br>
Mitigation: Confirm the active ClawHub account, current directory, included skill folders, and whether files contain secrets or private content before running broad commands. <br>
Risk: Suggested commands can target the wrong slug or version if local and remote skill names differ. <br>
Mitigation: Check local skill directories, lockfile listings, and ClawHub search or list output before installing, updating, or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlang-cn/skills-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose ClawHub CLI commands for local and remote skill management; users should review account, directory, and target skill scope before running bulk commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
