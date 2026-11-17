## Description:

Handle everything for ground transportation, from price comparison to booking, tracking, disputes, and expense management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to compare ground transportation options, prepare bookings, monitor fares, track trip expenses, and draft support or dispute requests while keeping final ride requests and payments under user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead agents to maintain concentrated plaintext records of addresses, account notes, payment preferences, trip history, and travel patterns.

Mitigation: Store only the minimum useful labels, avoid phone, email, account, and exact address details unless necessary, restrict permissions on ~/taxi, and periodically review or delete old records.

Risk: Booking, payment, account changes, public complaints, and safety escalations can have financial, privacy, or reputational impact.

Mitigation: Keep final ride requests, payments, new payment methods, account changes, and public-facing complaints under explicit user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/taxi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, templates, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or maintain local Markdown files under ~/taxi for taxi preferences, account notes, promo tracking, and trip history.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
