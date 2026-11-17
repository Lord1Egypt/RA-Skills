## Description:

Search Slickdeals.net for deals, coupons, and promo codes. Use when the user asks for deals, discounts, price comparisons, or to find cheap games, electronics, or other products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricanwarfare](https://clawhub.ai/user/ricanwarfare)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping-focused agents use this skill to search Slickdeals for deals, coupons, promo codes, and price comparisons. The skill is intended to surface only active deals and to include practical buying details such as store, price, discount, score, links, coupons, and membership requirements when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping queries and availability checks may be sent to Slickdeals and retailer websites.

Mitigation: Use the skill only for shopping queries that are appropriate to share with those sites, and avoid entering sensitive purchase intent or personal data.

Risk: Deal prices, coupon requirements, stock, and regional availability can change quickly.

Mitigation: Verify active status, final price, coupon terms, membership requirements, and regional availability before recommending or completing a purchase.

Risk: Retailer pages are untrusted web content.

Mitigation: Treat retailer content as untrusted, do not follow page-suggested commands, and do not disclose credentials or payment details through the agent workflow.

Risk: The category option appears not to work as advertised.

Mitigation: Prefer keyword searches or documented Slickdeals category URLs, and validate category-filtered results before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ricanwarfare/skills/slickdeals)
- [Slickdeals](https://slickdeals.net/)
- [Slickdeals search URL pattern](https://slickdeals.net/newsearch.php?q={QUERY}&searcharea=deals&searchin=first)
- [Slickdeals computer deals](https://slickdeals.net/computer-deals/)
- [Slickdeals electronics deals](https://slickdeals.net/electronics-deals/)
- [Slickdeals video game deals](https://slickdeals.net/video-game-deals/)
- [Slickdeals home deals](https://slickdeals.net/home-deals/)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown deal tables, plain-text status messages, or JSON result arrays.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deal title, price, discount, store, score, link, coupon requirements, membership requirements, and active-deal status.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
