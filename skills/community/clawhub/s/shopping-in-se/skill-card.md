## Description:

Help the user shop online at Swedish e-commerce sites, add products to cart, complete checkout, and handle Klarna, Stripe, or Adyen payment flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoqi](https://clawhub.ai/user/caoqi)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to delegate shopping on trusted Swedish e-commerce sites, including product search, recipient-detail entry, cart operations, and payment confirmation after explicit approval.

### Deployment Geography for Use:

Sweden

## Known Risks and Mitigations:

Risk: The skill handles raw payment credentials and can control checkout payment frames.

Mitigation: Use only a designated payment card, require explicit approval before purchase, and show the final merchant, amount, item, and recipient details before submitting payment.

Risk: The skill reads private recipient and payment files from the user's environment.

Mitigation: Require explicit approval before reading private files and limit file access to the documented recipient and designated payment-card files.

Risk: Broad browser-control techniques in cross-origin payment pages can submit sensitive checkout actions.

Mitigation: Restrict shopping to trusted domains, avoid paid search ad links, and keep payment interactions scoped to known providers such as Klarna, Stripe, and Adyen.

## Reference(s):

- [CDP Coordinate Click](references/cdp-click.md)
- [Trusted Shopping Sites](references/trusted-sites.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with browser actions, inline code, shell commands, and confirmation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include order details, merchant links, recipient confirmation, and screenshots of order confirmation pages.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
