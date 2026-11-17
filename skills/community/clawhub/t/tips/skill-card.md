## Description:

Recognizes tipping, appreciation, and gift-giving intent, collects and validates a tip amount, asks for user confirmation, and delegates payment creation to a payment skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sayxxx](https://clawhub.ai/user/sayxxx)

### License/Terms of Use:

MIT-0

## Use Case:

External assistants and commerce agents use this skill to handle user requests to tip, appreciate, or send a gift by validating the amount, confirming intent, and passing a tip order to a payment flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The payment flow does not itself bind or verify the intended recipient or payment provider, which can create under-scoped financial authorization.

Mitigation: Install only with a surrounding payment system that supplies and verifies the recipient and provider; users should confirm the amount, recipient, and payment link domain before paying.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown and structured payment-skill parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Collects an amount greater than 0 and no more than 10000 yuan; passes amount, order_type, and description to a payment skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
