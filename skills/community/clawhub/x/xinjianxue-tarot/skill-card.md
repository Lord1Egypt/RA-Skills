## Description:

Guides users through one of 50 tarot spreads, collects their chosen card numbers, and provides an interpretation using the returned cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill for reflective tarot readings about relationships, work, interpersonal situations, or choices. It selects a suitable spread, obtains the user's card numbers, and explains the returned cards; the skill excludes medical, legal, investment, and life-or-death conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags unexpected payment-wallet setup and paid-service steps, including installation of unpinned payment software, as outside the skill's stated tarot purpose.

Mitigation: Explain the payment requirement, wallet setup, package source and version, and fee before installation or authorization; independently verify those details before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-tarot)
- [API contract](artifact/references/api.md)
- [Payment flow](artifact/references/payment.md)
- [Reading framework](artifact/references/reading.md)
- [Spread list](artifact/references/spreads.md)
- [Tarot service endpoint](https://api.xinjianxue.com/api/xinjianxue/aipay/tarot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tarot reading with card positions, interpretations, a conclusion, and an actionable suggestion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Card names and orientations follow the returned result. A successful reading costs CNY 6 and uses a payment flow.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
