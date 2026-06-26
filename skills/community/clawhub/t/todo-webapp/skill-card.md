## Description: <br>
Deploys a local TODO web app that reads and writes Markdown TODO files, serves a LAN-accessible interface, supports live updates, toggles task checkboxes, archives completed tasks, and can auto-start on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwhowa](https://clawhub.ai/user/jwhowa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and operate a private LAN web UI for viewing, editing, and archiving tasks stored in TODO.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The web app exposes an unauthenticated editor for local TODO files on the LAN. <br>
Mitigation: Run it only on a trusted private network, or bind it to localhost or add authentication and origin checks before broader exposure. <br>
Risk: The Archive Done action modifies TODO.md and appends completed tasks to TODO-done.md. <br>
Mitigation: Review TODO.md sensitivity and keep backups before using archive operations. <br>
Risk: The macOS launchd setup can keep the editor running persistently after boot or crashes. <br>
Mitigation: Enable auto-start only when persistent access is intended and document how to unload or remove the LaunchAgent. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jwhowa/todo-webapp) <br>
- [Preview screenshot](https://i.imgur.com/noOCejM.jpeg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JavaScript code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for a zero-dependency Node.js TODO web app that reads and writes local Markdown files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
