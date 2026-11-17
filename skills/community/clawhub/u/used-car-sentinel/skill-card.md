## Description:

Screens used-car listings offline using VIN checks, mileage and price estimates, risk flags, and an inspection checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Used-car buyers and their agents use this skill to screen listings, check VIN consistency, compare estimated mileage and price, and prepare questions and an inspection checklist before visiting a seller or paying a deposit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic pricing and mileage estimates may misrepresent a particular car or local market.

Mitigation: Treat the estimates as rough guidance; compare local listings and verify mileage with service records.

Risk: A VIN check and screening verdict cannot establish title, vehicle identity, or mechanical condition.

Mitigation: Check the title and vehicle-history report, match the VIN on the car and paperwork, and obtain a professional inspection before purchase or deposit.

## Reference(s):

- [VIN Math, Market Model & Inspection Rationale](references/vin-math.md)
- [ClawHub release](https://clawhub.ai/voronindenis5/skills/used-car-sentinel)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text listing assessment, negotiation points, and inspection checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline; includes mileage and price estimates, risk flags, and a GREEN/YELLOW/RED screening verdict]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
