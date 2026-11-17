## Description:

AI travel-planning assistant for Chinese-language users that helps collect traveler details, analyze destinations, and produce personalized travel plans, safety notes, food suggestions, accommodation and transport guidance, and packing lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuyifeiruichuang](https://clawhub.ai/user/zhuyifeiruichuang)

### License/Terms of Use:

MIT-0

## Use Case:

External users planning travel in Chinese-language contexts use this skill to structure itinerary decisions, compare destination conditions, and generate practical recommendations. It is oriented toward family and general consumer travel planning, with special attention to health, weather, transportation, lodging, food, safety, and packing needs.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill asks by default for sensitive health and reproductive information.

Mitigation: Collect only travel-relevant optional details, avoid names, medical record numbers, prescription identifiers, insurance details, and unnecessary reproductive or treatment information.

Risk: The skill can provide medical-style travel advice without sufficient safeguards.

Mitigation: Frame health content as general travel information, recommend professional medical advice for personal medical decisions, and prioritize conservative safety warnings for elevated travel risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuyifeiruichuang/skills/travelassistant)
- [Health assessment travel guide](references/健康评估.md)
- [Seasonal destination guide](references/季节目的地指南.md)
- [Clothing guide](references/穿衣指南.md)
- [Packing checklist](references/行李清单.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown with tables and lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include destination analysis, itinerary recommendations, health and safety notes, food suggestions, accommodation and transport guidance, and packing checklists.]

## Skill Version(s):

1.0.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
