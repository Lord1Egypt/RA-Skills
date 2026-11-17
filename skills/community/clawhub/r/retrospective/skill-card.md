## Description:

Runs a structured weekly agent retrospective that analyzes wins, failures, skill gaps, cron health, and configuration issues from the last seven days.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidfurlong](https://clawhub.ai/user/davidfurlong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate a weekly self-review that records concrete wins, struggles, skill gaps, configuration issues, and prioritized action items. The skill is intended to create a markdown retrospective file and update persistent memory with key findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically creates a recurring weekly agent job that can access memory and configuration context.

Mitigation: Make scheduling opt-in, show the exact schedule and payload before creation, and provide clear disable and removal instructions.

Risk: The skill reviews sensitive configuration areas and persistent memory.

Mitigation: Prohibit reading or writing raw secrets, and limit retrospective output to evidence needed for operational review.

Risk: Broad natural-language triggers may cause the skill to run when the user did not intend a full retrospective.

Mitigation: Use explicit invocation phrases or require confirmation before running retrospective collection and updates.

## Reference(s):

- [Retrospective Anti-Patterns](references/anti-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/davidfurlong/skills/retrospective)
- [Publisher Profile](https://clawhub.ai/user/davidfurlong)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown retrospective report with tables, prioritized action items, and optional scheduling instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated retrospective file and may update persistent memory when executed by an agent.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
