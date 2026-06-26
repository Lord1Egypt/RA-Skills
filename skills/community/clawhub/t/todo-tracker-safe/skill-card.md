## Description: <br>
Secure TODO tracker with input validation and safe file operations for task management across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GothicFox](https://clawhub.ai/user/GothicFox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add, complete, remove, list, and summarize local TODO items across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TODO entries are stored in a persistent local file and may be summarized automatically. <br>
Mitigation: Do not put secrets or sensitive information in TODO entries, and review summaries before sharing them outside the local workspace. <br>
Risk: The TODO_FILE setting controls which file the script edits and can rewrite that configured file. <br>
Mitigation: Set TODO_FILE only to a dedicated TODO document and avoid pointing it at unrelated important files. <br>


## Reference(s): <br>
- [TODO Tracker (Safe) on ClawHub](https://clawhub.ai/GothicFox/todo-tracker-safe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain shell output and Markdown TODO file entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local TODO file configured by TODO_FILE, defaulting to ~/.openclaw/workspace/TODO.md.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
