## Description: <br>
Provides agent-guided countdown timers, reminders, Pomodoro sessions, and basic parallel timer management using local background execution and completion notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and independent developers use this skill to have an agent set local countdown timers, reminder messages, Pomodoro intervals, and multiple parallel timers without blocking the active session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill text includes unrelated writing, marketing, and title-generation routing language that could cause it to activate outside timer and reminder tasks. <br>
Mitigation: Install or enable it only for timer, reminder, and Pomodoro workflows, and review routing descriptions before deployment. <br>
Risk: The skill requires command execution, background timers, and process management, including commands that can terminate running sessions. <br>
Mitigation: Require user confirmation for process termination, monitor active timer sessions, and restrict execution to trusted local environments. <br>
Risk: Reminder messages may contain user-provided context that appears in local notifications or logs. <br>
Mitigation: Avoid placing secrets, credentials, or sensitive personal data in reminder text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/timer-alert-tool-free) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and structured status-response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reminder text, timer-management guidance, and command patterns for background timer execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
