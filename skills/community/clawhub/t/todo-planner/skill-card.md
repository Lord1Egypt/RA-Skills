## Description: <br>
Organize todos with priorities, deadlines, and weekly views. Use when adding tasks, planning agendas, tracking progress, reviewing overdue items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Todo Planner to capture, prioritize, review, search, and export local command-line todo entries for personal or work planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Bash script on the user's machine. <br>
Mitigation: Install and run it only when comfortable executing the bundled script in a trusted local shell. <br>
Risk: Todo entries, logs, and exports are stored as local plaintext files. <br>
Mitigation: Do not store passwords, secrets, or highly sensitive personal or work information in entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/todo-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; script output is plain text and exports can be JSON, CSV, or TXT.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores plaintext logs and generated exports locally under ~/.local/share/todo-planner/.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
