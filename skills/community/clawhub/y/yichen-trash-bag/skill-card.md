## Description: <br>
Yichen Trash Bag is an e-commerce customer-service skill that helps shoppers with trash-bag recommendations, specifications, pricing context, promotions, shipping, after-sales guidance, and wholesale inquiries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liubuq-sys](https://clawhub.ai/user/liubuq-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and store operators use this skill to answer Yichen Trash Bag product, pricing, promotion, logistics, returns, and bulk-purchase questions with guidance grounded in the bundled reference files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installers configure daily automatic updates and can overwrite an existing local skill folder. <br>
Mitigation: Install from a reviewed, pinned release when possible, inspect files before use, back up any existing skill folder, and remove the scheduled updater if automatic changes are not desired. <br>
Risk: Product prices, promotions, shipping terms, and store policies may change after the bundled reference files are published. <br>
Mitigation: Treat commercial details as guidance, read the relevant reference file before answering, and tell shoppers that final prices and offers are determined by the store checkout page. <br>
Risk: The skill can describe after-sales policies but cannot execute refunds, returns, replacements, or complaint handling. <br>
Mitigation: Route transactional requests to the store customer-service channel or platform backend and avoid promising direct operational actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liubuq-sys/yichen-trash-bag) <br>
- [Brand Reference](references/brand.md) <br>
- [Business Information Reference](references/business-info.md) <br>
- [Services Reference](references/services.md) <br>
- [Promotions Reference](references/promotions.md) <br>
- [FAQ Reference](references/faq.md) <br>
- [Shipping Reference](references/shipping.md) <br>
- [Wholesale Reference](references/wholesale.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Conversational text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers should be grounded in the bundled reference files for product details, prices, promotions, shipping, and policies.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
