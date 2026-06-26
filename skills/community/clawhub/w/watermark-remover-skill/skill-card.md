## Description: <br>
This skill helps an agent submit user-selected images to a local watermark-removal GUI through configured input and output folders, then return the processed file paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muxiazi](https://clawhub.ai/user/muxiazi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to automate watermark-removal jobs through an already-running local GUI for images they own or have permission to modify. It is intended for single-image and batch workflows where the agent can place files in a monitored input directory and read results from the configured output directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can be misused on images the user does not own or have permission to modify. <br>
Mitigation: Use the skill only for authorized images and confirm rights before processing shared or third-party media. <br>
Risk: The skill depends on a separate local GUI and exact input/output folder configuration, so jobs may fail or time out when the GUI is closed, monitoring is disabled, or paths differ. <br>
Mitigation: Run the built-in check command before processing and keep dedicated, matching folders configured in both the GUI and config file. <br>
Risk: Using the move option can remove originals from their source location. <br>
Mitigation: Prefer copy mode, keep backups of important images, and use move mode only when deletion of the source files is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muxiazi/watermark-remover-skill) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands, optional JSON result files, and processed image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local GUI program with directory monitoring enabled and configured input/output folders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
