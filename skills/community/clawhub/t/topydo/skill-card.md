## Description: <br>
topydo helps agents manage todo.txt task lists through the topydo CLI, including adding, listing, completing, prioritizing, tagging, organizing, and configuring tasks with dependencies, dates, recurrence, projects, and contexts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bastos](https://clawhub.ai/user/bastos) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and todo.txt users use this skill to ask an agent for topydo commands and workflow guidance for local task management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: topydo commands can change local task data by deleting, archiving, editing, sorting, or completing tasks. <br>
Mitigation: Preview matching tasks first and confirm exact task IDs or filters before allowing data-changing commands to run. <br>
Risk: Installing or invoking the topydo CLI from an untrusted source can expose the user to unsafe local command behavior. <br>
Mitigation: Install topydo only from a trusted package source and review generated commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bastos/topydo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
