## Description:

Calculate sleep-cycle-aligned wake-up times when the user says "晚安" or asks for best wake-up times, recommending several options with the best option first and top recommendations before 09:00 on workdays and before 11:00 on weekends or China public holidays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nathanshan](https://clawhub.ai/user/nathanshan)

### License/Terms of Use:


## Use Case:

External users use this skill to get concise wake-up time recommendations based on sleep-cycle timing, bedtime, and workday or China public holiday constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations rely on generic sleep-cycle timing and may not reflect an individual user's medical needs or actual sleep quality.

Mitigation: Present the output as practical scheduling guidance and avoid treating it as medical advice.

Risk: The skill assumes Chinese-language output and China public holiday handling, which may not match every user's locale.

Mitigation: Confirm locale, workday, or holiday assumptions when the user's context differs from China.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nathanshan/skills/sleep-wakeup-advisor)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Concise Markdown-style bullet list with wake-up times]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language response template; ranks 3-, 4-, 5-, and 6-cycle wake-up options with a 15-minute sleep-onset buffer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
