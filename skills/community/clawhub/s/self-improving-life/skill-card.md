## Description:

Helps users assess life satisfaction across health, relationships, work, finances, growth, leisure, and routines, then identify imbalances and practical next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and coaching-oriented agents use this skill for life wheel reviews, burnout prevention, routine resets, transition planning, and turning vague dissatisfaction into small measurable actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included quick assessment script saves personal life-assessment answers to a local Markdown report by default.

Mitigation: Run the script only in a private directory, avoid entering details that should not be retained, and review or delete generated reports after use.

Risk: The skill can involve sensitive health, relationship, work, and finance reflections.

Mitigation: Keep recorded details minimal unless the user explicitly wants a durable log.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/self-improving-life)
- [README](artifact/README.md)
- [Life wheel assessment template](artifact/assets/LIFE_WHEEL_TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell-script interaction and local Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for sensitive self-assessment scores and may generate local life-assessment Markdown files when the included script is run.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
