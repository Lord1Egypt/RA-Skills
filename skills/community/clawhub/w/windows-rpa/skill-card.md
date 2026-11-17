## Description:

Enables agents on Windows to automate desktop applications through mouse, keyboard, screenshot, image recognition, window management, clipboard, application launch, and shell-command tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qgyz9613](https://clawhub.ai/user/qgyz9613)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent control Windows desktop applications, capture screen state, manage windows, interact with the clipboard, and run local commands when browser automation is not suitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrary shell and run_app actions can execute local commands with the user's Windows privileges.

Mitigation: Run the skill in a low-privilege or sandboxed Windows account and require explicit approval for every shell or run_app action.

Risk: Screenshot, get_state, and clipboard-read actions can expose secrets, private documents, or other sensitive desktop content.

Mitigation: Avoid using the skill while sensitive content is visible or copied, and require explicit approval before screenshot, clipboard-read, and get_state actions.

Risk: Mouse and keyboard automation can affect the wrong application or window if the desktop state changes.

Mitigation: Confirm the target window and test workflows in an isolated environment before using the skill on important desktop sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qgyz9613/skills/windows-rpa)
- [Publisher Profile](https://clawhub.ai/user/qgyz9613)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON-like tool results with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets Windows only and may produce saved screenshot files when screenshot or state-capture tools are used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
