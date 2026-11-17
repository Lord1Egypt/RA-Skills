## Description:

Guides a tarot reading by choosing from 50 spreads, collecting the user's card numbers, and interpreting the returned cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill for reflective tarot readings about personal questions. It guides spread and card selection, interprets the results, and offers a practical next step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each successful reading costs ¥6 and requires buyer-side Alipay payment authorization.

Mitigation: Tell the user the merchant and amount before payment, require their authorization, and stop if they decline or payment fails.

Risk: Users could treat tarot interpretations as professional advice for high-stakes matters.

Mitigation: Do not answer medical, legal, investment, or life-and-death questions with tarot; direct users to appropriate professional support.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weixin97676414/skills/xinjianxue-tarot)
- [Tarot Service API](https://api.xinjianxue.com/api/xinjianxue/aipay/tarot)
- [Spread Catalog](artifact/references/spreads.md)
- [Reading Guidance](artifact/references/reading.md)
- [Payment Instructions](artifact/references/payment.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Conversational tarot reading with spread-position interpretations and practical suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not provide readings for medical, legal, investment, or life-and-death questions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
