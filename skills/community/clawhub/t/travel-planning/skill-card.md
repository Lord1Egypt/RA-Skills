## Description:

Plan trips with itineraries, multi-city routing, budget optimization, family logistics, packing lists, and visa timelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to plan and manage trips through itineraries, booking checklists, budgets, packing lists, traveler details, and deadline reminders. It supports destination wishlists, family or group logistics, multi-city routing, and local markdown records of travel preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist travel preferences, trip records, traveler details, and document references in local markdown, which may expose sensitive travel or identity-related information if over-collected.

Mitigation: Store only minimal travel details, avoid passport numbers, insurance policy numbers, medical details, payment details, and full booking confirmations, and periodically review or delete ~/travel-planning/.

Risk: Cross-session activation preferences may cause the assistant to engage on travel topics more broadly than expected.

Mitigation: Set activation to only when asked unless the user explicitly wants proactive travel reminders.

Risk: Travel timelines, visa guidance, passport-validity notes, and cost-saving estimates can vary by destination, date, and traveler circumstances.

Mitigation: Verify travel requirements, booking policies, and deadlines against official destination, carrier, lodging, insurance, and government sources before making decisions.

## Reference(s):

- [Travel Planning ClawHub Page](https://clawhub.ai/ivangdavila/skills/travel-planning)
- [Skill Definition](artifact/SKILL.md)
- [Booking Guide](artifact/booking-guide.md)
- [Memory Template](artifact/memory-template.md)
- [Multi-City Planning](artifact/multi-city.md)
- [Packing Templates](artifact/packing-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown files and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local travel-planning records when the user agrees to track trips and preferences.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
