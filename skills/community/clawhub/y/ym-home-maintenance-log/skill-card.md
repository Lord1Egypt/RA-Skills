## Description:

Tracks home appliances and household equipment with purchase dates, warranty periods, maintenance cycles, upcoming maintenance reminders, and receipt recordkeeping guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Household users and assistants use this skill to create and update a home appliance maintenance ledger, estimate warranty and maintenance dates, and list upcoming overdue, 30-day, and 90-day reminders. It is also useful for distinguishing user-safe recordkeeping and surface-level maintenance from tasks that require a professional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store home device details when the user asks it to create or update a ledger.

Mitigation: Ask for explicit confirmation before creating or updating a ledger, and avoid storing unnecessary device, location, or purchase details.

Risk: Maintenance guidance could be mistaken for repair instructions for hazardous tasks.

Mitigation: For gas, electrical, refrigerant, disassembly, and high-work tasks, only direct the user to brand support or a qualified professional.

Risk: Estimated warranty and maintenance dates can be inaccurate when purchase dates, warranty terms, or device details are missing.

Mitigation: Clearly label default or estimated values and state that warranty conclusions depend on purchase evidence and official policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-home-maintenance-log)
- [Publisher profile](https://clawhub.ai/user/liuyuming0823)
- [Server-resolved GitHub provenance](https://github.com/liuyuming0823/ym-home-maintenance-log)
- [Maintenance cycle table](artifact/references/maintenance-cycle-table.md)
- [Ledger template](artifact/templates/ledger-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown ledger tables, reminder lists, receipt checklists, and concise maintenance guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, no network behavior, and optional user-directed record storage only.]

## Skill Version(s):

0.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
