## Description:

Practical vehicle maintenance and roadside emergency skills. Use when someone needs to change a tire, jump-start a battery, handle a breakdown, deal with a fender bender, or perform basic car maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

Drivers and agents assisting drivers use this skill to prepare for roadside emergencies, follow basic vehicle maintenance checklists, and respond to flats, dead batteries, breakdowns, overheating, and minor collisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release uses an unpinned npx install path.

Mitigation: Use a pinned and reviewed installer before deployment.

Risk: The skill defines persistent vehicle, reminder, and accident fields that may contain sensitive details.

Mitigation: Avoid storing police report numbers, insurance claim numbers, precise accident locations, or other sensitive incident details unless retention and deletion controls are understood.

Risk: Roadside repair and accident guidance can be safety-critical if applied in traffic, heat, electrical, brake, or lifting scenarios.

Mitigation: Prioritize immediate personal safety, emergency services, the vehicle owner's manual, roadside assistance, or a qualified mechanic when conditions are unsafe or uncertain.

## Reference(s):

- [Vehicle Survival Kit on ClawHub](https://clawhub.ai/howtousehumans/skills/vehicle-survival-kit)
- [AAA Foundation for Traffic Safety](https://aaafoundation.org)
- [National Highway Traffic Safety Administration](https://www.nhtsa.gov)
- [Anthropic: Labor market impacts of AI](https://www.anthropic.com/research/labor-market-impacts)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown checklists and step-by-step instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include localized emergency numbers, road rules, measurement units, vehicle details, reminder state, and incident documentation fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
