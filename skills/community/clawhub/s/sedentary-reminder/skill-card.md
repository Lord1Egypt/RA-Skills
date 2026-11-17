## Description:

Designs practical sedentary-break reminder systems with strong timing logic for timing, deferral, focus or meeting adaptation, presence context, natural reminder copy, and recurring reminder plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linhucong814-cyber](https://clawhub.ai/user/linhucong814-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and automation builders use this skill to design sedentary-break reminders that account for sitting duration, work state, presence, interruption cost, and user controls. It helps produce reminder copy, timing policies, heartbeat or cron-friendly plans, state-update rules, and break-detection guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may maintain a local reminder state file and map user chat controls into state updates.

Mitigation: Review the state fields before integration, keep edits limited to sedentary reminder data, and confirm user control commands before enabling automated writeback.

Risk: Presence, idle, lock, sleep, or activity signals can be incomplete or wrong, which may cause reminders at poor times or missed reminders.

Mitigation: Use conservative defaults, suppress reminders when presence is uncertain or away, honor cooldowns, and allow manual pause, resume, and break confirmation controls.

Risk: Sedentary-break reminders can be mistaken for medical, posture, or safety advice.

Mitigation: Keep output general, avoid diagnosis or treatment claims, and recommend professional advice for pain, injury, rehabilitation, or medical questions.

## Reference(s):

- [Sedentary Reminder on ClawHub](https://clawhub.ai/linhucong814-cyber/skills/sedentary-reminder)
- [Chinese reminder library](references/reminder-copy-zh.md)
- [English reminder library](references/reminder-copy-en.md)
- [Chinese integration guide](references/integration-guide-zh.md)
- [Heartbeat template](references/heartbeat-template-zh.md)
- [Heartbeat state rules](references/heartbeat-state-rules-zh.md)
- [User controls guide](references/user-controls-zh.md)
- [Break detection guide](references/break-detection-zh.md)
- [Direct state editing guide](references/direct-state-editing-zh.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, plain text, JSON snippets, and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-language reminder output unless bilingual output is explicitly requested; recurring reminders should rotate copy and respect cooldowns, quiet windows, presence, and user controls.]

## Skill Version(s):

1.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
