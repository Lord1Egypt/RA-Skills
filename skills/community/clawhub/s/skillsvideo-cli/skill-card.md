## Description: <br>
SkillsVideo CLI guides agents to use the skillsvideo CLI for AI image and video generation across the skills.video model catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colorhook](https://clawhub.ai/user/colorhook) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and terminal agents use this skill to install or invoke the skillsvideo CLI, inspect model capabilities, submit image or video generation tasks, and download generated artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to run an unpinned remote shell installer before using the CLI. <br>
Mitigation: Review or verify the installer before execution and install only when skills.video and the target machine are trusted. <br>
Risk: Image and video generation can consume paid credits or run under an unintended account or workspace. <br>
Mitigation: Confirm the active account or workspace and get explicit user approval before paid generation runs. <br>
Risk: Broad local agent installation can update multiple local agent roots unexpectedly. <br>
Mitigation: Avoid broad install-skill --target all usage unless the user intends to update every supported local agent installation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/colorhook/skillsvideo-cli) <br>
- [skills.video](https://skills.video) <br>
- [skills.video CLI installer](https://skills.video/cli/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands, CLI output guidance, and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded image or video files when generation commands are run with output flags.] <br>

## Skill Version(s): <br>
0.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
