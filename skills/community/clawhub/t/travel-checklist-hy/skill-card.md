## Description:

根据目的地、日期、天气、交通方式和同行人生成个性化出行清单、待办事项与旅行提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocxf](https://clawhub.ai/user/cryptocxf)

### License/Terms of Use:

MIT-0

## Use Case:

旅行者可根据行程和个人需求制作可勾选的行李清单、出发及返程待办和安全提醒，也可更新已有清单状态。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outdated entry, medication, baggage or carrier rules could lead to incorrect travel preparations.

Mitigation: Check current official sources and mark uncertain requirements for verification.

Risk: Connecting travel accounts may expose itinerary details or sensitive credentials.

Mitigation: Request consent before connecting accounts, read only minimal itinerary fields, and do not request or store passport numbers, payment details, API keys or tokens.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cryptocxf/skills/travel-checklist-hy)
- [Checklist rules](artifact/references/checklist-rules.md)
- [Data access and fallback](artifact/references/data-access.md)
- [Output template](artifact/references/output-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown checklist and travel memo]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checkable, prioritized packing items; time-based tasks; conditional reminders and items awaiting official verification.]

## Skill Version(s):

1.0.0 (source: server release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
