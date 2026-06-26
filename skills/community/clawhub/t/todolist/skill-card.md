## Description: <br>
Manage macOS Reminders through AppleScript, including adding, listing, completing, deleting, searching, and creating reminder lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manifoldor](https://clawhub.ai/user/manifoldor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Mac users and their agents use this skill to manage reminders and todo lists in the native macOS Reminders app through clear shell-script actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fuzzy matching for complete and delete actions may affect the first partial reminder match. <br>
Mitigation: List matching reminders before completing or deleting items, and use specific reminder titles when issuing commands. <br>
Risk: Reminder changes can sync to other Apple devices through iCloud. <br>
Mitigation: Confirm destructive actions with the user before deleting reminders or changing shared lists. <br>
Risk: The skill requires local permission to control macOS Reminders. <br>
Mitigation: Install only when the user expects agent access to Reminders and approve macOS automation prompts deliberately. <br>


## Reference(s): <br>
- [Todo List for MacOS on ClawHub](https://clawhub.ai/manifoldor/todolist) <br>
- [Publisher profile: manifoldor](https://clawhub.ai/user/manifoldor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS Reminders access; results may reflect iCloud-synced reminder state.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
