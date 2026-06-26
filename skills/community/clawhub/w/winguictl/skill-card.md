## Description: <br>
Windows desktop automation CLI for controlling windows, simulating mouse and keyboard input, capturing screenshots, and automating desktop applications when explicitly requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[easyteacher](https://clawhub.ai/user/easyteacher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to inspect and control authorized Windows desktop applications through window management, UI snapshots, element finding, input actions, screenshots, waits, and clipboard operations. It is intended for explicit, user-approved desktop automation tasks where the target window and action are verified before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a live Windows desktop and WeChat session, including sending messages, posting content, deleting data, exporting private data, and making contact changes. <br>
Mitigation: Require explicit confirmation of the target window, recipient, content, file path, deletion, export, call, or contact change before executing any action. <br>
Risk: Mouse, keyboard, hotkey, and window-close actions may affect the wrong application or cause data loss if the desktop state changes. <br>
Mitigation: Use exact window IDs, focus the target window, take a fresh snapshot, preview with dry-run when available, and re-verify state after each action. <br>
Risk: Screenshots, OCR, snapshots, and clipboard reads may expose sensitive visible text, files, or clipboard contents. <br>
Mitigation: Close or minimize sensitive applications, avoid broad history/contact/file extraction unless specifically authorized, and treat captured desktop content as sensitive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/easyteacher/winguictl) <br>
- [Security Guidelines](references/SECURITY.md) <br>
- [Action Commands](references/action.md) <br>
- [Window Commands](references/window.md) <br>
- [Snapshot Commands](references/snapshot.md) <br>
- [Find Commands](references/find.md) <br>
- [Output Format](references/output-format.md) <br>
- [Dependencies](references/dependencies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command examples, with CLI results commonly returned as JSON or boundary-marked text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for Windows hosts with python3 and desktop automation dependencies; OCR and image matching require optional packages.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
