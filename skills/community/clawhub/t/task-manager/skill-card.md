## Description: <br>
SQLite-based task management with priority, tags, and stats. Database stored in skill directory for natural isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rare](https://clawhub.ai/user/rare) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI-agent users use this skill to create, update, filter, and summarize local tasks with priorities, tags, due dates, statuses, and persistent SQLite storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task titles, descriptions, and update history are stored persistently in the local SQLite database. <br>
Mitigation: Avoid putting secrets or sensitive personal data in task titles or descriptions, and treat the skill directory's data folder as persistent local storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rare/task-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with shell command examples; the bundled CLI prints task records, status updates, and task statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Task data is stored persistently in a local SQLite database under the skill directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
