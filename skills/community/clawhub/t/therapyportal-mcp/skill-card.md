## Description:

Read a TherapyNotes client portal for appointments, paperwork, forms, balances, payment receipts, secure messages, and downloadable documents using the user's signed-in portal session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Clients or caregivers use this skill to check upcoming therapy appointments, requested paperwork, balances, receipts, and secure-message threads. It can also retrieve completed forms or payment receipts as PDF files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanners report that the authenticated helper can make unrestricted portal changes and expose sensitive records despite its read-only description.

Mitigation: Treat the read-only claim as unverified; avoid use unless needed and review the behavior before connecting it to a portal account.

Risk: Portal responses can contain sensitive mental-health records, including records about minors, and the security scan was incomplete.

Mitigation: Use projected commands, select only the fields needed, and avoid printing unfiltered demographic responses or sharing records unnecessarily.

## Reference(s):

- [TherapyPortal endpoints reference](references/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/chrischall/skills/therapyportal-mcp)

## Skill Output:

**Output Type(s):** [JSON data, PDF files]

**Output Format:** [Projected portal records in JSON; downloaded forms and receipts in PDF format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive mental-health, identifying, and payment information; limit output to the information needed for the request.]

## Skill Version(s):

0.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
