## Description: <br>
Xiao Habit Tracker provides habit-tracking workflows for check-ins, statistics, achievements, reminders, and data export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage daily habits: add habits, record check-ins, inspect streak and completion statistics, view achievements, configure reminders, and export habit data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A required curl binary is declared even though reviewed artifacts contain no executable code; future cloud sync or notification behavior could introduce network activity. <br>
Mitigation: Confirm why curl is required and review future versions for documented network behavior before deployment. <br>
Risk: Habit exports, reminders, and cloud sync may involve personal routine data. <br>
Mitigation: Review data storage, sync, notification, and export handling before using the skill with sensitive personal information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/xiao-habit-tracker) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code was found in the reviewed artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
