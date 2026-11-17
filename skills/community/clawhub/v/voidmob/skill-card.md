## Description:

Helps agents obtain SMS verification numbers, rent dedicated numbers, provision mobile proxies, and purchase travel eSIM data through VoidMob with user approval before spending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voidmob](https://clawhub.ai/user/voidmob)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers use this skill for SMS on their own accounts, receiving messages on rented numbers, authorized mobile-IP testing, and travel data plans. Purchases use a prepaid balance and require approval for each charge.

### Deployment Geography for Use:

Global; number, proxy, and eSIM availability varies by country and plan.

## Known Risks and Mitigations:

Risk: The API key can spend the account's prepaid balance.

Mitigation: Store the key securely, keep the balance small, and obtain a fresh explicit approval for every purchase, renewal, or top-up.

Risk: Uncertain purchase results could lead to duplicate charges or unwanted renewals.

Mitigation: Reuse the same idempotency key when retrying a purchase, check existing orders before another attempt, and enable auto-renew only when requested.

Risk: SMS numbers and mobile proxies can be misused for third-party account abuse or evading platform safeguards.

Mitigation: Restrict use to authorized accounts and tasks; decline bulk account creation, ban evasion, and rate-limit avoidance.

## Reference(s):

- [VoidMob homepage](https://voidmob.com)
- [VoidMob API reference](https://dashboard.voidmob.com/api-reference.html)
- [SMS and rentals](references/sms.md)
- [Dedicated numbers](references/numbers.md)
- [Mobile proxies](references/proxies.md)
- [eSIM plans](references/esim.md)
- [Errors and recovery](references/errors.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell examples and service results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SMS codes, number details, proxy credentials, or eSIM installation details; share sensitive results only with the user.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
