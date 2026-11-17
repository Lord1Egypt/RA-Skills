## Description:

Tianshu Huangdao helps agents answer Traditional Chinese calendar, auspicious-date, I Ching, fortune, zodiac, five-elements, and naming questions, with PayPal-gated paid reports for full fortune, hexagram, and naming workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makclaw](https://clawhub.ai/user/makclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to provide Traditional Chinese responses for huangli date selection, Chinese zodiac and fortune readings, I Ching hexagram lookup, and Chinese naming suggestions. Paid flows require user confirmation, PayPal payment, and a paypal_order_id before full reports are requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts sinodata.io and may require birth dates or naming details for fortune and naming reports.

Mitigation: Use the skill only when users are comfortable sharing those details with the service, and avoid collecting unnecessary personal information.

Risk: Paid fortune, I Ching, and full naming reports require PayPal payment before the report is requested.

Mitigation: Confirm the paid action with the user, complete the PayPal flow, and pass a valid paypal_order_id only after payment succeeds.

Risk: The skill is intended to produce Traditional Chinese calendar, fortune, and naming guidance that users may interpret as advisory.

Mitigation: Present outputs as cultural or informational guidance and avoid treating them as professional, financial, legal, or medical advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/makclaw/skills/tianshu-huangdao)
- [Tianshu Huangdao API gateway](https://sinodata.io)
- [Huangdao help endpoint](https://sinodata.io/v1/huangdao/help)
- [Packaged skill instructions](artifact/SKILL.md)
- [Packaged calendar, naming, I Ching, five-elements, and zodiac datasets](artifact/data/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Configuration]

**Output Format:** [Traditional Chinese text or Markdown with API request guidance and returned report data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid fortune, I Ching, and full naming outputs require a PayPal order ID; free calendar, naming preview, and help responses do not require payment.]

## Skill Version(s):

1.0.7 (source: evidence.release.version and target metadata; artifact files include older embedded versions)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
