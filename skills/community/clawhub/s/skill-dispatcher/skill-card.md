## Description:

Proactive skill router that helps an agent map user intent to available skills through a decision tree, enhancer layer, anti-forget checks, and coverage-gap detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miantiao1231](https://clawhub.ai/user/miantiao1231)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep installed skills visible during task routing, detect uncovered skills, and guide onboarding of newly installed skills into a routing table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a broad router that can persistently affect future agent behavior and skill selection.

Mitigation: Install only when an always-on routing helper is intended, and review routing-table changes before deployment.

Risk: The artifact includes guidance for core-file edits, registry searches, self-editing, repackaging, reinstalling, memory writes, and mandatory output tags.

Mitigation: Require explicit approval or remove these behaviors before operational use, following the server security guidance.

## Reference(s):

- [New Skill Onboarding Protocol](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/miantiao1231/skills/skill-dispatcher)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with routing tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require local customization of routing tables, trigger phrases, and covered-skill registry entries before use.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
