## Description: <br>
Handle everything for ground transportation, from price comparison to booking, tracking, disputes, and expense management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to compare ground transportation options, prepare ride bookings, track trip expenses, and draft support or dispute messages. It is intended to keep the user in control of final ride and payment confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local taxi memory can contain sensitive home or work addresses, trip history, receipts, account identifiers, and promo details. <br>
Mitigation: Keep only necessary ride details, avoid passwords and full payment data, mask exact addresses when possible, and review the local ~/taxi files periodically. <br>
Risk: Booking assistance can prepare ride or payment steps that still require user judgment. <br>
Mitigation: Have the user confirm ride details, driver or vehicle information, payment actions, and any new account verification before a booking is finalized. <br>
Risk: Complaint drafts or social escalation can expose account-specific ride, receipt, or location details. <br>
Mitigation: Remove private identifiers and exact addresses before sharing support messages publicly, and use private support channels for sensitive disputes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/taxi) <br>
- [Booking Workflows](artifact/booking.md) <br>
- [City Coverage](artifact/cities.md) <br>
- [Fare Estimation & Savings](artifact/fares.md) <br>
- [Memory Setup](artifact/memory-template.md) <br>
- [Problem Resolution](artifact/problems.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklists, tables, templates, and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local memory templates, trip logs, fare comparisons, booking steps, and complaint drafts for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
