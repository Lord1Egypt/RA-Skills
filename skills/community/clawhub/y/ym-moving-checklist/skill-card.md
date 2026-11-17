## Description:

Generates a dated moving plan with box labels, special packing lists, address changes, utility transfers, handover checks, timelines, and risk reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan residential moves by date, home size, move type, and family constraints. It produces a practical checklist covering packing, transfers, handover tasks, and post-move follow-up without providing legal advice or DIY gas/electrical instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad packing-related triggers may activate the skill for some non-moving questions.

Mitigation: Confirm that the user is planning a move before applying the full moving checklist workflow.

Risk: Utility transfer, school, vehicle, and government-office procedures can vary by location.

Mitigation: Ask users to verify local requirements with the relevant utility, bank, school, government office, or service provider.

Risk: Requests about gas, electrical, air-conditioner work, deposits, or contract disputes can exceed the skill's safe scope.

Mitigation: Give only general preparation and evidence-preservation guidance, direct technical work to qualified professionals, and direct legal questions to appropriate professional or local consumer channels.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/liuyuming0823/ym-moving-checklist)
- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-moving-checklist)
- [Timeline task reference](artifact/references/timeline-tasks.md)
- [Address transfer reference](artifact/references/address-transfers.md)
- [Moving checklist output template](artifact/templates/moving-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown checklist with tables and sectioned task lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Seven-section moving checklist; requires separate fragile/valuable, must-carry, and last-packed-first-unpacked lists.]

## Skill Version(s):

0.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
