## Description:

Help users buying a home solar panel system calculate panel wattage, battery Ah, inverter VA, and charge controller type from their load, location, and grid situation - region-aware and brand-neutral.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbazex](https://clawhub.ai/user/arbazex)

### License/Terms of Use:

MIT-0

## Use Case:

External homeowners and residential solar buyers use this skill to gather energy, roof, location, grid, and backup requirements, then receive a structured solar system buying specification with explicit sizing calculations. It is intended for component selection and quote evaluation, not electrical installation, wiring, or commissioning advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The consultation may request location, roof, and household energy details that can be sensitive when overly specific.

Mitigation: Use approximate details where possible, such as city or region instead of an exact address, approximate roof area, and approximate energy usage.

Risk: Solar system recommendations can be unsafe if treated as installation, wiring, or commissioning instructions.

Mitigation: Use the skill for buying specifications and quote evaluation only, and rely on a certified solar installer or licensed electrician for installation work.

Risk: Regional product availability, certifications, utility rules, and feed-in policies may change.

Mitigation: Verify current local certifications, utility interconnection requirements, and product availability before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arbazex/skills/solar-panel-home-system-buying-consultant)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational text followed by structured Markdown recommendations with calculations and numbered product suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows key sizing formulas and calculations; product suggestions are capped at five and should be verified for current regional availability before purchase.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
