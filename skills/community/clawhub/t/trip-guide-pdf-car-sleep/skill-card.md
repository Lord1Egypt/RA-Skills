## Description:

Research, plan, revise, and deliver car-sleep travel guides as HTML/PDF with verified overnight parking, charging, toilet access, next-morning route anchors, and formal copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allensu0314](https://clawhub.ai/user/allensu0314)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce car-sleep travel guides that prioritize verified overnight anchors, charging, toilets, route timing, screenshots, and fallback logic. It is intended for trips where lodging is removed or the traveler plans to sleep in a vehicle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parking, charging, toilet, and route details may be outdated or wrong when used for real travel decisions.

Mitigation: Verify schedule-critical claims with current maps, official scenic pages, structured listings, and visible parking or access evidence before relying on them.

Risk: A 24-hour parking or charging location may be mistaken for explicit permission to sleep in a vehicle overnight.

Mitigation: Label unverified locations as candidate night anchors and distinguish hard permission evidence from soft car-sleep or camping signals.

Risk: Changing a sleep point can invalidate downstream route timing and scenic order.

Mitigation: Recompute dependent legs, charger or toilet coverage, morning departure logic, and fallback points after every night-anchor change.

## Reference(s):

- [Source Selection for Car-Sleep Guides](artifact/references/source-selection.md)
- [QA Checklist for Car-Sleep Guides](artifact/references/qa-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/allensu0314/skills/trip-guide-pdf-car-sleep)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance, files]

**Output Format:** [Formal travel guide prose, usually drafted as HTML with optional PDF export and supporting screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes verified hard data, labeled soft signals, candidate overnight anchors, and fallback points.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
