## Description: <br>
团队任务管家 is a platform-neutral team task coordination skill that stores tasks in JSON files and supports natural-language task creation, reminders, overdue escalation, analytics, and multi-format export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djoldwang](https://clawhub.ai/user/djoldwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams and their agents use this skill to maintain shared task records, assign owners, send platform-neutral reminders, track progress, search tasks, produce statistics, and export task data. Host integrations provide member identity mapping, notification routing, and regional workday calendars. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent task files, task history, exports, and reminders can expose team work details or personal assignment data. <br>
Mitigation: Install only in workspaces where that storage and reminder behavior is acceptable; configure file permissions, retention expectations, export access, and notification routing before use. <br>
Risk: Ambiguous natural-language requests can create the wrong task, assignee, priority, or notification target. <br>
Mitigation: Require confirmation for ambiguous task creation, assignment, priority, deadline, and routing decisions, and use reliable member identity mapping from the host environment. <br>
Risk: Local JSON task storage can become inconsistent if writes fail or if multiple actors modify files without coordination. <br>
Mitigation: Use the documented read-modify-backup-write flow, preserve .bak files for recovery, scan archives when generating IDs, and avoid unsynchronized manual edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/djoldwang/team-tasks) <br>
- [Publisher profile](https://clawhub.ai/user/djoldwang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples, JSON data models, text templates, and export format specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local team task JSON files and can describe CSV, TXT, or JSON exports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
