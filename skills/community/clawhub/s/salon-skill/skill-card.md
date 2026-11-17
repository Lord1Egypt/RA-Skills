## Description:

A comprehensive skill for beauty salon operations covering hair, nails, skin services, appointments, service menus, client consultations, recommendations, and marketing content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhi152003](https://clawhub.ai/user/abhi152003)

### License/Terms of Use:

MIT-0

## Use Case:

Salon owners, front desk staff, and client-facing agents use this skill to handle appointment workflows, service and pricing questions, consultation intake, personalized recommendations, staff-facing reminders, and salon marketing copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect client contact details, appointment notes, and hair, skin, or nail concerns without a privacy note.

Mitigation: Add a privacy note that states what client data is collected, why, who can access it, and how long it is retained before production use.

Risk: Placeholder services, prices, currency, policies, staff names, and booking details may be inaccurate for a specific salon.

Mitigation: Replace placeholders with the salon's verified local service menu, policies, staff list, booking link, and contact details.

Risk: Broad activation language could trigger the skill for loosely related salon conversations.

Mitigation: Narrow the trigger text to explicit salon operation, booking, consultation, service-menu, staff scheduling, or marketing tasks.

## Reference(s):

- [Client Consultation & Intake Logic](artifact/references/consultation.md)
- [Service Menu & Pricing](artifact/references/services.md)
- [Salon Skill on ClawHub](https://clawhub.ai/abhi152003/skills/salon-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or conversational text with short messages, structured lists, tables, and platform-specific marketing copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; includes placeholders that must be localized before production use.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
