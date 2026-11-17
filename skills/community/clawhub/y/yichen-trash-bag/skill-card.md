## Description:

Yichen Trash Bag is a Chinese e-commerce customer-service skill for answering product, price, promotion, shipping, after-sales, and wholesale questions about Yichen trash bag products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubuq-sys](https://clawhub.ai/user/liubuq-sys)

### License/Terms of Use:

MIT-0

## Use Case:

External customers and store support agents use this skill to provide warm Chinese-language storefront assistance for Yichen trash bag selection, specifications, pricing, promotions, delivery, after-sales policy, and wholesale/OEM inquiries. The skill relies on bundled reference files for product and business details.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The installer paths execute mutable remote code and configure daily auto-update behavior.

Mitigation: Review installer scripts locally, use a pinned or verified archive, avoid one-line remote shell installation, and remove cron or scheduled-task auto-updates unless daily self-updates are explicitly desired.

Risk: Running installers with elevated privileges could expand the impact of script or update behavior.

Mitigation: Install as a normal user and do not run the shell or PowerShell installer with administrator or root privileges.

Risk: Product prices, promotions, and shipping details may change after the bundled reference files were published.

Mitigation: Read the relevant reference file before answering and state that final prices, promotions, and delivery terms are determined by the customer-facing order page or store support channel.

Risk: The skill can describe after-sales policies but cannot process refunds, replacements, or complaints directly.

Mitigation: Route refund, replacement, complaint, and account-specific cases to the store customer-service channel or platform self-service flow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liubuq-sys/skills/yichen-trash-bag)
- [Brand Introduction](references/brand.md)
- [Business Information](references/business-info.md)
- [Product Catalog](references/services.md)
- [Promotions](references/promotions.md)
- [Product FAQ](references/faq.md)
- [Shipping and Delivery](references/shipping.md)
- [Wholesale and OEM](references/wholesale.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language Chinese customer-service replies, optionally using short lists or tables for product details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the bundled references directory to be readable when answering business-data questions.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact version files list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
