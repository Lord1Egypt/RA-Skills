## Description: <br>
Generate styled QR images/cards for ClawHub skills so users can scan and install instantly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackleeio](https://clawhub.ai/user/jackleeio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to create scan-to-install QR cards for sharing ClawHub skills in chats, documentation, and social posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional PNG conversion can run unintended shell commands if a crafted output filename is used. <br>
Mitigation: Use trusted slug, title, GitHub, and output-path values only; prefer the default output path or run with --no-png until the conversion command is replaced with safer argument-array execution. <br>


## Reference(s): <br>
- [Skill QR Card on ClawHub](https://clawhub.ai/jackleeio/skill-qr-card) <br>
- [Design Guidelines](references/design-guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [SVG file with optional PNG file and MEDIA path output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a styled QR card for install-command, ClawHub URL, or GitHub URL payloads.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
