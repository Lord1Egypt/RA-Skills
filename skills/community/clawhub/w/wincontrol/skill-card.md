## Description: <br>
AI remote control for Windows desktop. Captures screen on-demand via POST request and provides an HTTP API for mouse/keyboard actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqshi13](https://clawhub.ai/user/qqshi13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Wincontrol to let an agent inspect and operate a local Windows desktop through screenshot capture and mouse or keyboard HTTP actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes screen capture and keyboard or mouse control on localhost without authentication. <br>
Mitigation: Run it only on a trusted single-user machine, keep the service bound to localhost, and stop it when the desktop-control session is finished. <br>
Risk: Local processes or browser pages able to reach the service may capture the screen or send desktop actions. <br>
Mitigation: Avoid running the service while browsing untrusted content or while other untrusted local processes are active. <br>
Risk: Screenshots can contain sensitive desktop content. <br>
Mitigation: Close or hide sensitive windows before capture and rely on the skill's shutdown cleanup after use. <br>


## Reference(s): <br>
- [Wincontrol ClawHub page](https://clawhub.ai/qqshi13/wincontrol) <br>
- [qqshi13 publisher profile](https://clawhub.ai/user/qqshi13) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes localhost HTTP API usage for screenshot capture and desktop input control.] <br>

## Skill Version(s): <br>
2.0.1 (source: CHANGELOG.md, skill.json, _meta.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
