## Description: <br>
Manages user schedules and task lists by adding, viewing, updating, deleting, and optionally setting reminders for tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h3avysword](https://clawhub.ai/user/h3avysword) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain a local schedule, prioritize tasks, inspect upcoming work by date range, and confirm updates or deletions before changes are made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Schedule details, notes, and deadlines are stored in a local workspace CSV file. <br>
Mitigation: Install only when local workspace storage is acceptable, and avoid entering sensitive schedule content unless the workspace is trusted. <br>
Risk: Update and delete operations can change or remove schedule entries. <br>
Mitigation: Review task IDs and confirmation prompts carefully before applying updates or deletions. <br>
Risk: Optional reminders depend on a separate reminder skill. <br>
Mitigation: Enable reminders only when the separate reminder skill is trusted and appropriate for the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/h3avysword/schedules-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text schedule summaries and confirmations, with local Python command invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores schedule details, deadlines, priorities, reminder flags, and notes in a workspace CSV file.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
