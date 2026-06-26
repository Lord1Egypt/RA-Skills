## Description: <br>
Create terminal screenshots, animated GIFs, or videos using VHS scripts for documentation, demos, and reproducible CLI visuals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricardodantas](https://clawhub.ai/user/ricardodantas) <br>

### License/Terms of Use: <br>
GPL-3.0 <br>


## Use Case: <br>
Developers and technical writers use this skill to create reproducible terminal screenshots, animated CLI demos, and video walkthroughs for documentation and tutorials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A tape file can hide setup or cleanup commands from the recording while still executing them. <br>
Mitigation: Review every .tape file before running it, especially sections between Hide and Show. <br>
Risk: Terminal recordings may expose tokens, private paths, production data, or other secrets. <br>
Mitigation: Use disposable working directories and avoid recording terminals that contain sensitive values or private environment context. <br>
Risk: Cleanup examples can remove local files if copied into a real project without adjustment. <br>
Mitigation: Replace cleanup commands with harmless placeholders or commands scoped to temporary directories. <br>


## Reference(s): <br>
- [VHS GitHub](https://github.com/charmbracelet/vhs) <br>
- [VHS Themes](https://github.com/charmbracelet/vhs/blob/main/THEMES.md) <br>
- [VHS Example Tapes](https://github.com/charmbracelet/vhs/tree/main/examples) <br>
- [ClawHub Skill Page](https://clawhub.ai/ricardodantas/terminal-screenshots) <br>
- [Publisher Profile](https://clawhub.ai/user/ricardodantas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and tape code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of .tape files and VHS commands that generate image, GIF, or video artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
