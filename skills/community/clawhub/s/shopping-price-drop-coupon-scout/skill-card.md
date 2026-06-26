## Description: <br>
Track product prices and surface official coupons or discounts without purchasing or account access. Use when a user wants price alerts, deal summaries, or coupon lists for specific items or retailers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to create read-only product price watchlists, identify official coupons or promo codes, and draft alert messages for selected products or retailers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prices, coupon eligibility, or expiration dates may be stale or vary by region. <br>
Mitigation: Use official retailer sources or user-provided exports, ask for region when needed, and include source, timestamp, eligibility, and expiration details in summaries. <br>
Risk: Users may provide sensitive retailer credentials, cookies, or payment details. <br>
Mitigation: Do not request or store login credentials, cookies, or payment data; use public promo pages or explicitly provided scoped API keys only. <br>
Risk: Automated collection can violate retailer terms or rate limits. <br>
Mitigation: Use official APIs, public promo pages, trusted alert webhooks, or user-provided data, and avoid prohibited scraping or checkout endpoints. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/codedao12/shopping-price-drop-coupon-scout) <br>
- [Overview](references/overview.md) <br>
- [Auth](references/auth.md) <br>
- [Endpoints](references/endpoints.md) <br>
- [Safety](references/safety.md) <br>
- [UX](references/ux.md) <br>
- [Webhooks](references/webhooks.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown watchlists, coupon lists, price summaries, and draft alert messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only suggestions; no purchases, checkout actions, payment handling, login, or cookie storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
