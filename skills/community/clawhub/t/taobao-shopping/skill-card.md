## Description:

Helps agents research Taobao products using public information, compare sellers, prices, reviews, and SKU risks, and prepare user-controlled cart and checkout handoff guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to research Taobao listings, compare options, assess seller and SKU risk, and prepare a manual pre-purchase checklist. It is intended for public visible information only; account state, checkout, order submission, and payment remain user-controlled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public shopping data such as price, stock, promotions, seller status, reviews, and delivery terms may change or vary by account, location, or time.

Mitigation: Treat the skill output as decision support and have the user verify final payable amount, stock, address-based delivery, coupon eligibility, return terms, invoice, and warranty before purchase.

Risk: Login, address, coupon, cart, checkout, order, and payment flows involve private account state or financial action.

Mitigation: Stop before those flows and require the user to complete any cart changes, checkout, order submission, and payment manually.

Risk: The skill may encounter requests for passwords, SMS codes, payment details, address details, or other account data while researching Taobao pages.

Mitigation: Do not collect or store those details; hand control back to the user whenever authentication, CAPTCHA, private account state, or payment information is required.

## Reference(s):

- [Public Browser Workflow for Taobao Shopping](references/browser-workflow.md)
- [Marketplace Guide](references/marketplace-guide.md)
- [Output Patterns](references/output-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown shopping summaries, comparison tables, risk notes, and handoff checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Taobao information and user-provided details; does not perform login, cart, checkout, order, or payment actions.]

## Skill Version(s):

2.1.3 (source: server release evidence, clawhub.json, package.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
