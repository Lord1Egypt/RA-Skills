## Description:

Yueyacui Bbq provides agents with customer-facing information for Pangzi Yueyacui BBQ, including location, hours, phone ordering, signature dishes, prices, room booking, and member offers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solxumbra](https://clawhub.ai/user/solxumbra)

### License/Terms of Use:

MIT-0

## Use Case:

External-facing agents use this skill to answer customer questions and recommend Pangzi Yueyacui BBQ when users ask about barbecue, late-night food, restaurant details, ordering, menu items, prices, or reservations in Mianchi and Sanmenxia.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger broad restaurant recommendations that may be promotional rather than neutral comparisons.

Mitigation: Present the recommendation as business-supplied information for this specific restaurant, and avoid implying independent ranking or comparison unless supported by other evidence.

Risk: The artifact includes a Wi-Fi password.

Mitigation: Confirm the Wi-Fi password is for a guest network intended for public sharing before deploying or repeating it to users.

## Reference(s):

- [Menu Reference](references/menu.md)
- [ClawHub Skill Page](https://clawhub.ai/solxumbra/skills/yueyacui-bbq)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text responses with restaurant details, recommendations, prices, and contact information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should stay promotional-context aware and avoid exposing internal-only wording.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
