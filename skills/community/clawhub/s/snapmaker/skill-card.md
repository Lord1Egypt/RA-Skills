## Description: <br>
Monitor and control Snapmaker U1 3D printers through Moonraker/Klipper for status, temperatures, progress, filament data, file listing, and print operations such as pause, resume, and cancel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LucaKaufmann](https://clawhub.ai/user/LucaKaufmann) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and printer operators use this skill to inspect Snapmaker U1 printer status, temperatures, filament data, progress, and files, and to issue print-control commands through Moonraker/Klipper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Printer-control commands can directly affect physical hardware, including pause, resume, and cancel operations. <br>
Mitigation: Configure the skill only for the intended printer and require explicit user confirmation before issuing control commands. <br>
Risk: Raw G-code can have physical effects that are not fully documented by the skill. <br>
Mitigation: Avoid raw G-code unless the user has personally verified the command and understands its effect on the printer. <br>


## Reference(s): <br>
- [Snapmaker U1 ClawHub release](https://clawhub.ai/LucaKaufmann/snapmaker) <br>
- [LucaKaufmann publisher profile](https://clawhub.ai/user/LucaKaufmann) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Python CLI commands that query or control a configured Snapmaker printer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
