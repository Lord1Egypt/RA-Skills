## Description: <br>
Taobao Shopping helps an agent evaluate public Taobao listings, sellers, SKUs, reviews, visible prices, promotions, return protections, and buy/wait/avoid decisions while keeping login, cart, checkout, order, and payment actions user-controlled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to research Taobao products from public listing evidence, compare seller and SKU risks, and produce a manual pre-purchase checklist. It is intended for decision support, not for changing account state or completing transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled documentation and metadata inconsistently mention cart or coupon actions that could affect a user's Taobao account. <br>
Mitigation: Use the skill only for public Taobao research and decision support; keep login, coupon claiming, cart changes, checkout, order submission, and payment manual. <br>
Risk: Taobao recommendations may be misleading when final price, coupons, SKU availability, delivery, or returns depend on private account or checkout-only conditions. <br>
Mitigation: Require the user to manually verify selected SKU, final payable amount, address-based delivery, coupon eligibility, stock, return policy, invoice, warranty, and payment before buying. <br>


## Reference(s): <br>
- [Taobao Shopping ClawHub listing](https://clawhub.ai/harrylabsj/skills/taobao-shopping) <br>
- [Browser Workflow](artifact/skills/taobao-shopping/references/browser-workflow.md) <br>
- [Marketplace Guide](artifact/references/marketplace-guide.md) <br>
- [Output Patterns](artifact/references/output-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, analysis] <br>
**Output Format:** [Markdown with verdict, evidence, risk, and final-check sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public-visible Taobao evidence and hands off account-state, checkout, and payment steps to the user.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
