## Description: <br>
Xiaozhi Im Reminder helps agents create consent-based learning reminders for review, action follow-up, and progress confirmation using spaced-repetition timing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qizhitang](https://clawhub.ai/user/qizhitang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, guardians, and learning-support agents use this skill to schedule authorized study reminders, task follow-ups, exploration prompts, and evening confirmation check-ins without enabling idle wakeups by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled reminders could become too frequent or disruptive. <br>
Mitigation: Use the documented pause, cancel, frequency adjustment, and quiet-hours controls before enabling or continuing reminders. <br>
Risk: Cross-skill coordination could expose more learning context than needed. <br>
Mitigation: Share only minimal authorized summaries and honor the documented opt-out command for sharing. <br>
Risk: The skill can propose reminders, but timed delivery depends on the host platform. <br>
Mitigation: Confirm that the deployment platform supports scheduled tasks and IM delivery before relying on reminders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qizhitang/xiaozhi-im-reminder) <br>
- [Ebbinghaus schedule reference](artifact/references/ebbinghaus-schedule.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with reminder schedules, control commands, sharing boundaries, and message templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reminder proposals and response guidance; actual reminder creation depends on explicit user consent and host-platform scheduling support.] <br>

## Skill Version(s): <br>
1.1.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
