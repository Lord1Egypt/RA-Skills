## Description:

Vehicle restriction query and reminder tool for Chinese cities. Query daily restrictions and set scheduled reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chandler0714](https://clawhub.ai/user/chandler0714)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Chinese vehicle restriction rules by city and plate number, and to manage local reminder entries for restriction checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vehicle plate, city, and reminder time can be stored locally in plaintext.

Mitigation: Avoid storing sensitive vehicle data on shared machines and review local file permissions before using reminders.

Risk: City and reminder support may be broader in documentation than in observed behavior.

Mitigation: Treat the skill as mainly a Beijing restriction query tool unless the target city and reminder workflow are independently tested.

Risk: Restriction results can rely on fallback data when online retrieval fails.

Mitigation: Verify important restriction decisions against the official traffic source before acting on them.

## Reference(s):

- [Beijing Traffic Management Bureau restriction page](https://jtgl.beijing.gov.cn/jgj/lszt/659722/660341/index.html)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON CLI output and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read online Beijing restriction data and may create local reminder configuration under the user's home directory.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
