## Description: <br>
Designs practical sedentary-break reminder systems with strong timing logic. Use when users want help deciding when to remind, how often to remind, when to defer, how to adapt to focus/meeting/presence context, and how to generate natural reminder copy or recurring reminder plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linhucong814-cyber](https://clawhub.ai/user/linhucong814-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and productivity-tool builders use this skill to design context-aware sit-break reminder timing, reminder copy, user controls, and heartbeat or cron-friendly reminder plans for work, study, and desk use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local reminder state could expose work-state, presence, pause, or activity-timing details if wired into heartbeat or automation. <br>
Mitigation: Keep memory/heartbeat-state.json local, review stored fields, and provide simple inspect, pause, undo, and reset controls. <br>
Risk: Direct state-editing behavior could change reminder settings unexpectedly if casual chat is treated as a command. <br>
Mitigation: Require clear user commands for state changes and confirm ambiguous pause, resume, profile, or work-state requests before updating state. <br>
Risk: Sedentary reminders may be mistaken for medical or posture-tracking advice. <br>
Mitigation: Keep guidance general, avoid diagnosis or treatment claims, and recommend professional advice for pain, injury, rehabilitation, or medical concerns. <br>
Risk: Poorly timed reminders can interrupt meetings, presentations, focus work, or unsafe moments. <br>
Mitigation: Use the skill's deferral, cooldown, presence, meeting, and focus-state rules before sending reminders. <br>


## Reference(s): <br>
- [久坐提醒 Break 识别规则](references/break-detection-zh.md) <br>
- [久坐提醒直改状态方案](references/direct-state-editing-zh.md) <br>
- [久坐提醒状态自更新规则](references/heartbeat-state-rules-zh.md) <br>
- [久坐提醒 Heartbeat 模板](references/heartbeat-template-zh.md) <br>
- [久坐提醒落地指南](references/integration-guide-zh.md) <br>
- [English sit-break reminder copy library](references/reminder-copy-en.md) <br>
- [中文久坐提醒文案库](references/reminder-copy-zh.md) <br>
- [久坐提醒用户控制说明](references/user-controls-zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with reminder copy, timing rules, and optional JSON-like state fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include single-language reminder variants, rotation sets, timing profiles, heartbeat state rules, and cron-friendly plans.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
