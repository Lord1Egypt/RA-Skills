## Description:

Use when buying or troubleshooting a room air conditioner — Manual-J-style BTU sizing from room geometry, sun exposure, insulation and occupancy, with the oversizing trap (short-cycling => no dehumidification), 110V vs 230V circuit checks, and noise/heat-pump guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Homeowners, renters, and other occupants can estimate the cooling capacity needed for a room, troubleshoot short-cycling, compare seasonal energy costs, and check purchase and installation factors for a window or portable air conditioner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Limited numerical validation can make results unreliable for invalid or non-positive inputs.

Mitigation: Enter positive input values and review the printed assumptions.

Risk: The sizing result is a rough estimate, and HVAC accuracy was not validated in this review.

Mitigation: Verify the selected unit's specifications and installation requirements before purchase.

Risk: An incompatible circuit or window installation may make a selected unit unsuitable or unsafe.

Mitigation: Check voltage, amperage, window fit, and installation requirements against the specific unit's documentation.

## Reference(s):

- [Window AC Sizing — Load Model, Short-Cycling, and Purchase Physics](references/load-model-and-purchase-physics.md)
- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/window-ac-sizer)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Plain-text room-load breakdowns, sizing verdicts, and seasonal cost estimates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses room measurements and user-provided equipment and energy-cost details; electrical and market-size examples are US-oriented.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
