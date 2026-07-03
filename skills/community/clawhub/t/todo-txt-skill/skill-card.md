## Description: <br>
Manage tasks, todos and reminders using the todo.txt CLI (todo.sh). Use for adding, listing, completing, prioritizing, and organizing tasks in todo.txt format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eaguilera23](https://clawhub.ai/user/eaguilera23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People running AI agents use this skill to manage a durable local todo.txt task list through natural-language requests that map to todo.sh commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled installer can download todo.txt CLI source, build it, run Homebrew or sudo installation commands, and write local configuration. <br>
Mitigation: Require explicit user approval before running the installer, Homebrew, git clone, make, sudo, or configuration-copy commands. <br>
Risk: Task-management commands can alter or delete local todo.txt data, including archive, delete, and force-mode actions. <br>
Mitigation: Review the intended todo.sh command with the user before destructive or force-mode operations, and list tasks after changes. <br>
Risk: The skill depends on local todo.sh behavior and local configuration, so results may vary across macOS, Linux, and user-specific todo.txt setups. <br>
Mitigation: Verify todo.sh installation and configuration before routine use, and use a temporary todo.txt file when testing. <br>


## Reference(s): <br>
- [todo.txt CLI](https://github.com/todotxt/todo.txt-cli) <br>
- [todo.txt format](https://github.com/todotxt/todo.txt) <br>
- [ClawHub skill page](https://clawhub.ai/eaguilera23/todo-txt-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify local todo.txt files and todo.sh configuration when executing task-management commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog, released 2026-06-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
