## Description:

Track product prices and surface official coupons or discounts without purchasing or account access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

External users use this skill to track prices for selected products, compare official coupons or promos, and draft alert messages without checkout, account login, or payment handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retailer terms or automated access limits may restrict price and coupon collection.

Mitigation: Use official retailer APIs, public promo pages, or user-provided exports, and avoid scraping or automation that violates retailer terms.

Risk: Shopping workflows can drift toward checkout, account access, or payment handling.

Mitigation: Keep the skill read-only: do not request login credentials, store cookies, handle payment details, add items to carts, or call purchase and checkout endpoints.

Risk: Prices and coupons can vary by region, eligibility, and expiration date.

Mitigation: Ask for region, currency, target price, retailer preferences, cadence, and timezone, then include source, eligibility, and expiration details in outputs.

## Reference(s):

- [Overview](references/overview.md)
- [Auth](references/auth.md)
- [Endpoints](references/endpoints.md)
- [Webhooks](references/webhooks.md)
- [UX](references/ux.md)
- [Troubleshooting](references/troubleshooting.md)
- [Safety](references/safety.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown watchlists, coupon summaries, and alert message drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only suggestions; no purchases, checkout actions, payment details, account login, or cookie storage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
