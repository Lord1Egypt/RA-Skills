## Description: <br>
Build or improve Telegram inline-button file browsers and menu-style navigators for browsing directories, paging lists, previewing files, returning to parent views, closing menus, or exposing copyable file paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Just-CJ](https://clawhub.ai/user/Just-CJ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create Telegram chat interfaces for browsing files inside a bounded workspace, previewing file contents, showing copyable paths, and sending selected files through Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The browser can expose or send local files from the selected root into Telegram chats. <br>
Mitigation: Keep the browser root limited to a non-sensitive workspace and avoid browsing home or system directories. <br>
Risk: Callback-looking text messages may be treated as browser commands without strong session checks. <br>
Mitigation: Use the skill only where callback handling is bound to the intended user or session, and avoid shared chats unless downloads require confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Just-CJ/telegram-file-browser) <br>
- [Interaction Patterns](references/interaction-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, Python snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Telegram message payloads and button matrices for file-browser interactions.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
